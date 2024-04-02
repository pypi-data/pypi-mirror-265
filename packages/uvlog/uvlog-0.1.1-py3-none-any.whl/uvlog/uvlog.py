"""Python logging utilities."""

import io
import logging
import os
import queue
import sys
import traceback
from abc import abstractmethod
from collections import ChainMap
from contextvars import ContextVar  # noqa: pycharm bug?
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from json import dumps
from random import random
from pathlib import Path
from threading import Thread
from typing import (
    Any,
    BinaryIO,
    Callable,
    ClassVar,
    Collection,
    Literal,
    Mapping,
    Optional,
    Protocol,
    TypedDict,
    cast,
    no_type_check,
    Type,
    Dict,
    List,
)
from urllib.parse import urlparse
from weakref import WeakValueDictionary

__all__ = [
    "LOG_CONTEXT",
    "BASIC_CONFIG",
    "LogRecord",
    "Logger",
    "Handler",
    "Formatter",
    "TextFormatter",
    "JSONFormatter",
    "StreamHandler",
    "QueueHandler",
    "add_formatter_type",
    "add_handler_type",
    "set_logger_type",
    "add_handler",
    "add_formatter",
    "remove_handler",
    "get_logger",
    "configure",
    "clear",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]

LOG_CONTEXT: ContextVar[Optional[Dict[str, Any]]] = ContextVar(
    "LOG_CONTEXT", default=None
)  #: default log context


class Stream(Enum):
    """List of default log streams."""

    stdout = sys.stdout.buffer
    stderr = sys.stderr.buffer


DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
CRITICAL = "CRITICAL"

_root_logger_name = ""
_default_timespec = "seconds"
_default_format = "{asctime} | {level} | {name} | {message} | {extra} | {ctx}"
_formatter_types: Dict[str, Type["Formatter"]] = {}


class _DictConfig(TypedDict, total=False):
    loggers: Dict[str, dict]
    handlers: Dict[str, dict]
    formatters: Dict[str, dict]


BASIC_CONFIG: _DictConfig = {
    "loggers": {_root_logger_name: {}},
    "handlers": {
        Stream.stderr.name: {},
        Stream.stdout.name: {},
    },
    "formatters": {
        "text": {"class": "TextFormatter"},
        "json": {"class": "JSONFormatter"},
    },
}  #: default log configuration

_LevelName = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
_handler_types: Dict[str, Type["Handler"]] = {}
_handlers: Dict[str, "Handler"] = {}
_formatters: Dict[str, "Formatter"] = {}
_loggers_persistent: Dict[str, "Logger"] = {}
_loggers_temp: WeakValueDictionary = WeakValueDictionary()
_loggers: ChainMap = ChainMap(_loggers_persistent, _loggers_temp)
_name_to_level: Dict[_LevelName, int] = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


@dataclass
class LogRecord:
    """Log record object.

    A log record object is created when a log method of a logger is called.
    """

    __slots__ = ('name', 'level', 'levelno', 'asctime', 'filename', 'lineno', 'func', 'message', 'exc_info', 'extra', 'ctx')

    name: str
    """Logger name"""

    level: _LevelName
    """Log record level name"""

    levelno: int
    """Log record level number"""

    asctime: datetime
    """Timestamp of record creation"""

    message: str
    """Log message"""

    exc_info: Optional[Exception]
    """Exception (if any)"""

    extra: Optional[Mapping[str, Any]]
    """Log extra information provided in kwargs"""

    ctx: Optional[Mapping[str, Any]]
    """Log contextual information"""

    filename: Optional[str]
    """Filename of the caller"""

    func: Optional[str]
    """Function name of the caller"""

    lineno: Optional[int]
    """Source code line number of the caller"""

    def __getitem__(self, item: str, /):
        return getattr(self, item)


class Formatter(Protocol):
    """Log formatter interface.

    It's a protocol class, i.e. one doesn't need to inherit from it to create a valid formatter.
    """

    @abstractmethod
    def format_record(self, record: LogRecord, /) -> bytes: ...


class Handler(Protocol):
    """Log handler interface.

    It's a protocol class, i.e. one doesn't need to inherit from it to create a valid handler.
    """

    @abstractmethod
    def handle(self, record: LogRecord, /) -> None: ...

    @abstractmethod
    def set_level(self, level: _LevelName, /) -> None: ...

    @abstractmethod
    def set_formatter(self, fmt: Formatter, /) -> None: ...

    @abstractmethod
    def set_destination(self, dest: str, /) -> None:
        """Set a handler destination.

        Since only one destination allowed for a single handler, this method must call :py:func:`~uvlog.add_handler`
        to ensure that a handler for this destination doesn't exist. It also should call
        :py:func:`~uvlog.remove_handler` for its previous destination before adding a new one.

        Example:

        .. code-block:: python

            def set_destination(self, dest: str, /) -> None:
                remove_handler(self._dest)
                self._dest = dest
                ...
                add_handler(dest)

        """
        # remove_handler(self.dest)
        # add_handler(dest, self)

    @abstractmethod
    def close(self) -> None:
        """Close the handler including all connections to its destination.

        This method is called automatically at exit for each added handler by the :py:func:`~uvlog.clear` function.
        """


def add_formatter_type(typ: Type[Formatter], /) -> None:
    _formatter_types[typ.__name__] = typ


def add_handler_type(typ: Type[Handler], /) -> None:
    _handler_types[typ.__name__] = typ


def add_formatter(name: str, formatter: Formatter, /) -> None:
    _formatters[name] = formatter


def add_handler(destination: str, handler: Handler, /) -> None:
    if destination in _handlers:
        raise ValueError(
            f"handler already exists for this destination: {destination}\n\n"
            f"Fix: ensure you don't have two handlers with the same destination, or use "
            f"`uvlog.remove_handler(<dest>)` method to remove a conflicting handler"
        )
    _handlers[destination] = handler


def remove_handler(destination: str, /) -> None:
    handler = _handlers.pop(destination, None)
    if handler is not None:
        handler.close()


@dataclass
class Logger:
    """Logger object.

    It can be used almost like a standard Python logger, except that it allows passing keyword arguments
    directly to `extra`:

    .. code-block:: python

        main_logger = uvlog.get_logger('app')
        logger = main_logger.get_child('my_service')

        logger.debug('debug message', debug_value=42)
        logger.error('error happened', exc_info=Exception())

    """

    name: str
    """Logger name"""

    level: _LevelName = "INFO"
    """Logging level"""

    handlers: List[Handler] = field(default_factory=list)
    """List of attached log handlers"""

    sample_rate: float = 1.0
    """Log records sample rate which determines a probability at which a record should be sampled.
    
    Sample rate is not considered for levels above 'INFO'. Values >= 1 disable the sampling mechanism.
    """

    sample_propagate: bool = True
    """By default the sampling mechanism is contextual meaning that if there's a non-empty log context,
    the log chain is marked 'sampled' as it sampled by the first logger in a chain. Once a record is 'sampled' the
    log chain cannot be *unsampled*, i.e. all subsequent loggers will be forced to sample it as well.
    It allows to preserve an entire request log chain in the logs and not just some random not connected logs.
    """

    context: ContextVar[Optional[Dict[str, Any]]] = LOG_CONTEXT
    """Log context variable - useful for contextual data,
    see `contextvars <https://docs.python.org/3/library/contextvars.html>`_
    """

    capture_trace: bool = False
    """Capture traceback for each call such as line numbers, file names etc. — may affect performance"""

    _levelno: int = field(init=False, default=0)
    _parent: Optional["Logger"] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self._levelno = _name_to_level[self.level]
        self.sample_rate = min(max(0.0, self.sample_rate), 1.0)

    def set_level(self, level: _LevelName, /) -> None:
        self._levelno = _name_to_level[level]
        self.level = level

    def get_child(self, name: str, /, *, persistent: bool = False) -> "Logger":
        """Get or create a child logger inheriting all the logger settings.

        .. attention::

            Note that by default a new logger is not *persistent*, i.e. it will be eventually garbage collected if
            there are no live references to it.
        """
        if "." in name:
            raise ValueError(
                '"." symbol is not allowed in logger names when calling `get_child` directly\n\n'
                "Fix: if you want to create a chain of loggers "
                "use `uvlog.get_logger()` function instead"
            )
        if name in _loggers:
            return _loggers[name]
        child_name = name if self.name == _root_logger_name else f"{self.name}.{name}"
        child_logger = _logger_type(
            name=child_name,
            level=self.level,
            context=self.context,
            handlers=[*self.handlers],
            capture_trace=self.capture_trace,
        )  # noqa
        child_logger._parent = self
        if persistent:
            _loggers_persistent[name] = child_logger
        else:
            _loggers_temp[name] = child_logger
        return child_logger

    def critical(
        self,
        msg: str,
        /,
        exc_info: Optional[Exception] = None,
        stack_info=None,
        stacklevel=1,
        **kws,
    ) -> None:
        if self._levelno > logging.CRITICAL:
            return
        ctx = self.context.get()
        if ctx and self.sample_rate < 1:
            ctx["_sample"] = True
        fn, lno, func, _ = (
            _find_caller(stack_info, stacklevel)
            if self.capture_trace
            else (None, None, None, None)
        )
        record = LogRecord(
            self.name,
            "CRITICAL",
            logging.CRITICAL,
            datetime.now(),
            msg.format_map(kws),
            exc_info,
            kws if kws else None,
            ctx,
            fn,
            func,
            lno,
        )
        for handler in self.handlers:
            handler.handle(record)

    def error(
        self,
        msg: str,
        /,
        exc_info: Optional[Exception] = None,
        stack_info=None,
        stacklevel=1,
        **kws,
    ) -> None:
        if self._levelno > logging.ERROR:
            return
        ctx = self.context.get()
        if ctx and self.sample_rate < 1:
            ctx["_sample"] = True
        fn, lno, func, _ = (
            _find_caller(stack_info, stacklevel)
            if self.capture_trace
            else (None, None, None, None)
        )
        record = LogRecord(
            self.name,
            "ERROR",
            logging.ERROR,
            datetime.now(),
            msg.format_map(kws),
            exc_info,
            kws if kws else None,
            ctx,
            fn,
            func,
            lno,
        )
        for handler in self.handlers:
            handler.handle(record)

    def warning(
        self,
        msg: str,
        /,
        exc_info: Optional[Exception] = None,
        stack_info=None,
        stacklevel=1,
        **kws,
    ) -> None:
        if self._levelno > logging.WARNING:
            return
        ctx = self.context.get()
        if ctx and self.sample_rate < 1:
            ctx["_sample"] = True
        fn, lno, func, _ = (
            _find_caller(stack_info, stacklevel)
            if self.capture_trace
            else (None, None, None, None)
        )
        record = LogRecord(
            self.name,
            "WARNING",
            logging.WARNING,
            datetime.now(),
            msg.format_map(kws),
            exc_info,
            kws if kws else None,
            ctx,
            fn,
            func,
            lno,
        )
        for handler in self.handlers:
            handler.handle(record)

    def info(
        self,
        msg: str,
        /,
        exc_info: Optional[Exception] = None,
        stack_info=None,
        stacklevel=1,
        **kws,
    ) -> None:
        if self._levelno > logging.INFO:
            return
        ctx = self.context.get()
        if ctx and self.sample_rate < 1:
            _sample = ctx.get("_sample")
            if _sample is None:
                _sample = random() < self.sample_rate
                if self.sample_propagate:
                    ctx["_sample"] = _sample
            if not _sample:
                return
        fn, lno, func, _ = (
            _find_caller(stack_info, stacklevel)
            if self.capture_trace
            else (None, None, None, None)
        )
        record = LogRecord(
            self.name,
            "INFO",
            logging.INFO,
            datetime.now(),
            msg.format_map(kws),
            exc_info,
            kws if kws else None,
            ctx,
            fn,
            func,
            lno,
        )
        for handler in self.handlers:
            handler.handle(record)

    def debug(
        self,
        msg: str,
        /,
        exc_info: Optional[Exception] = None,
        stack_info=None,
        stacklevel=1,
        **kws,
    ) -> None:
        if self._levelno > logging.DEBUG:
            return
        ctx = self.context.get()
        if ctx and self.sample_rate < 1:
            _sample = ctx.get("_sample")
            if _sample is None:
                _sample = random() < self.sample_rate
                if self.sample_propagate:
                    ctx["_sample"] = _sample
            if not _sample:
                return
        fn, lno, func, _ = (
            _find_caller(stack_info, stacklevel)
            if self.capture_trace
            else (None, None, None, None)
        )
        record = LogRecord(
            self.name,
            "DEBUG",
            logging.DEBUG,
            datetime.now(),
            msg.format_map(kws),
            exc_info,
            kws if kws else None,
            ctx,
            fn,
            func,
            lno,
        )
        for handler in self.handlers:
            handler.handle(record)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


_logger_type = Logger


def set_logger_type(typ: Type["Logger"], /) -> None:
    global _logger_type
    _logger_type = typ


def get_logger(name: str = _root_logger_name, /, *, persistent: bool = False) -> Logger:
    """Get an existing logger or create a new one.

    :param name: logger full name, for example 'app.services.my_service', by default returns the root logger
    :param persistent: make this logger persistent and store it forever

    .. attention::

        Contrary to Python default logging module, this function by default produces a non-persistent logger unless it
        has been created using `uvlog.configure()`. This means that once no existing references exist for this logger,
        it will be garbage-collected.
    """
    if name in _loggers:
        return _loggers[name]
    if name == _root_logger_name:
        _loggers[_root_logger_name] = logger = _logger_type(_root_logger_name)
        return logger
    split_name = name.split(".")
    parent = _loggers[_root_logger_name]
    for parent_name in split_name[:-1]:
        parent = parent.get_child(parent_name, persistent=persistent)
    logger = parent.get_child(split_name[-1], persistent=persistent)
    return logger


def _dumps_default(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


def _dumps_bytes(obj) -> bytes:
    # patched standard json dumps method to dump bytestring
    # in reality you'd rather want to use a faster json library like `orjson` etc.
    return dumps(obj, default=_dumps_default).encode("utf-8")


# python traceback extraction methods - a ripoff of the standard logging library method

_srcfile = os.path.normcase(_dumps_bytes.__code__.co_filename)


def _find_caller(stack_info=None, stacklevel: int = 1):
    """Find the stack frame of the caller so that we can note the source file name, line number, function name."""
    f = sys._getframe(1)  # noqa
    if f is None:
        return "(unknown file)", 0, "(unknown function)", None
    while stacklevel > 0:
        next_f = f.f_back
        if next_f is None:
            break
        f = next_f
        filename = os.path.normcase(f.f_code.co_filename)
        is_internal_frame = filename == _srcfile or (
            "importlib" in filename and "_bootstrap" in filename
        )
        if not is_internal_frame:
            stacklevel -= 1
    co = f.f_code
    return co.co_filename, f.f_lineno, co.co_name, None


@dataclass
class TextFormatter:
    """Text log formatter.

    Creates human-readable log output.

    Formatter settings can be set directly.

    .. code-block:: python

        _formatter = TextFormatter()
        _formatter.timestamp_separator = ' '

    """

    timespec: str = field(init=False, default=_default_timespec)
    """Precision for ISO timestamps,
    see `datetime.isoformat() <https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat>`_"""

    timestamp_separator: str = field(init=False, default="T")
    """Timestamp separator for ISO timestamps,
    see `datetime.isoformat() <https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat>`_"""

    format: str = field(init=False, default=_default_format)
    """Log record format, a python f-string,
    the available keys can be seen in :py:class:`~uvlog.LogRecord` type
    """

    def format_record(self, record: LogRecord, /) -> bytes:
        message = self.format.format_map(
            {
                "asctime": record.asctime.isoformat(
                    timespec=self.timespec, sep=self.timestamp_separator
                ),
                "level": record.level,
                "name": record.name,
                "message": record.message,
                "filename": record.filename,
                "func": record.func,
                "lineno": record.lineno,
                "extra": record.extra,
                "ctx": record.ctx,
            }
        )
        if record.exc_info is not None:
            exc_info = record.exc_info
            message += "\n" + self._format_exc(
                type(exc_info), exc_info, exc_info.__traceback__
            )
        return message.encode("utf-8")

    @staticmethod
    def _format_exc(error_cls, exc, stack, /) -> str:
        sio = io.StringIO()
        traceback.print_exception(error_cls, exc, stack, None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s

    def __str__(self):
        return f"<{self.__class__.__name__}>"


@dataclass
class JSONFormatter:
    """JSON log formatter.

    To change the default `dumps` function assign it to the class attribute:

    .. code-block:: python

        import orjson

        JSONFormatter.serializer = orjson.dumps

    Formatter settings can be set directly.

    .. code-block:: python

        _formatter = JSONFormatter()
        _formatter.exc_pass_locals = True

    """

    serializer: ClassVar[Callable[[Any], bytes]] = field(
        init=False, default=_dumps_bytes
    )
    """Serializer function - a class attribute"""

    keys: Collection[str] = field(
        init=False,
        default=(
            "name",
            "level",
            "asctime",
            "message",
            "exc_info",
            "extra",
            "ctx",
            "filename",
            "lineno",
            "func",
        ),
    )
    """List of serialized log record keys,
    the available keys can be seen in :py:class:`~uvlog.LogRecord` type"""

    exc_pass_locals: bool = field(init=False, default=False)
    """Pass locals dict in exception traceback (don't use it unless you're sure your logs are secure)"""

    exc_pass_globals: bool = field(init=False, default=False)
    """Pass globals dict in exception traceback (don't use it unless you're sure your logs are secure)"""

    def __post_init__(self):
        self.keys = set(self.keys)

    def format_record(self, record: LogRecord, /) -> bytes:
        data = {
            k: getattr(record, k) for k in self.keys if getattr(record, k) is not None
        }
        exc_info = cast(Exception, data.pop("exc_info", None))
        if exc_info and "exc_info" in self.keys:
            error_cls, exc, _ = type(exc_info), exc_info, exc_info.__traceback__
            if hasattr(exc, "serialize"):
                data["exc_info"] = exc.serialize()
            else:
                data["exc_info"] = {
                    "message": str(exc),
                    "type": error_cls.__name__,
                    "data": exc.__dict__,
                }
                if exc.__traceback__:
                    frame = exc.__traceback__.tb_frame
                    data["exc_info"]["traceback"] = tb = {
                        "lineno": frame.f_lineno,
                        "func": frame.f_code.co_name,
                    }
                    if self.exc_pass_locals:
                        tb["locals"] = frame.f_locals
                    if self.exc_pass_globals:
                        tb["globals"] = frame.f_globals

        return self.__class__.serializer(data)

    def __str__(self):
        return f"<{self.__class__.__name__}>"


@dataclass
class StreamHandler:
    """Logging handler.

    A simple stream handler which immediately writes a log record to the write buffer. It provides the best performance.
    However, in server applications you may want to use `uvlog.QueueStreamLogger`
    to ensure your code is not blocking due to intensive logging.
    """

    terminator: ClassVar[bytes] = b"\n"
    """Delimiter between log records"""

    _level: _LevelName = field(init=False, default="DEBUG")
    _dest: str = field(init=False, default=Stream.stderr.name)
    _formatter: Formatter = field(default_factory=TextFormatter)
    _levelno: int = field(init=False, default=0)
    _stream: Optional[BinaryIO] = field(init=False, default=None)

    def __post_init__(self):
        self._levelno = _name_to_level[self._level]
        self._stream = None

    def handle(self, record: LogRecord, /) -> None:
        """Immediately write a log record to the write buffer."""
        if record.levelno < self._levelno:
            return
        if self._stream is None:
            self._stream = self._open_stream()
        record_bytes = self._formatter.format_record(record)
        try:
            self._stream.write(record_bytes + self.terminator)
        except Exception:  # noqa: acceptable
            self._handle_error(record_bytes)

    def set_level(self, level: _LevelName, /) -> None:
        self._level = level
        self._levelno = _name_to_level[level]

    def set_formatter(self, formatter: Formatter, /) -> None:
        self._formatter = formatter

    def set_destination(self, dest: str, /) -> None:
        """Set log destination (file stream).

        Pre-configured destinations are: 'stdout' and 'stderr'.

        Both plain and URL file formats are acceptable and normalized into a path string:

        - logs.txt - relative path
        - /logs.txt - absolute path
        - file:///logs.txt - absolute path in file URL format
        """
        if dest not in (Stream.stdout.name, Stream.stderr.name):
            _path = Path(urlparse(dest).path)
            _path.parent.mkdir(parents=True, exist_ok=True)
            _path.touch(exist_ok=True)
        remove_handler(dest)
        add_handler(dest, self)
        self._dest = dest
        self._stream = None

    def close(self) -> None:
        """Close the handler including all connections to its destination.

        This method is called automatically at exit for each added handler by the :py:func:`~uvlog.clear` function.
        """
        if self._stream and not self._stream.closed:
            self._stream.flush()
            if self._stream not in (sys.stderr.buffer, sys.stdout.buffer):
                self._stream.close()
        self._stream = None

    def _open_stream(self) -> BinaryIO:
        """Open a file stream."""
        if self._dest == Stream.stderr.name:
            return Stream.stderr.value
        elif self._dest == Stream.stdout.name:
            return Stream.stdout.value
        else:
            return open(self._dest, "ab")

    @staticmethod
    @no_type_check
    def _handle_error(message: bytes, /) -> None:
        """Handle an error which occurs during an emit() call.

        This method is a loose ripoff of the standard python logging error handling mechanism.
        """
        _, exc, tb = sys.exc_info()
        try:
            sys.stderr.write("--- Logging error ---\n")
            traceback.print_exception(
                exc, limit=None, file=sys.stderr, value=exc, tb=tb
            )
            sys.stderr.write("Call stack:\n")
            frame = exc.__traceback__.tb_frame
            while frame:
                frame = frame.f_back
            if frame:
                traceback.print_stack(frame, file=sys.stderr)
            try:
                sys.stderr.write(f"Message: {message}\n")
            except RecursionError:
                raise
            except Exception:  # noqa: acceptable
                sys.stderr.write(
                    "Unable to print the message and arguments"
                    " - possible formatting error.\nUse the"
                    " traceback above to help find the error.\n"
                )
        except OSError:
            pass
        finally:
            del exc

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self._dest} / {self._formatter}>"


@dataclass
class QueueHandler(StreamHandler):
    """Logging handler with an internal queue.

    This handler uses a queue and a separate thread providing at least some concurrency during intensive logging
    workload. It has a worse overall performance than :py:class:`~uvlog.StreamHandler` but may be beneficial if you have
    concurrent code such as a server application.

    You may want to set :py:attr:`~uvlog.QueueHandler.queue_size`
    to some reasonable value considering your application workload.

    The handler uses a separate thread to write logs to the buffer via the :py:meth:`~uvlog.QueueHandler.write_loop`
    method. Note that this handler doesn't use any internal locks,
    because it's expected by design that each handler has its own destination.
    """

    _sentinel = None

    queue_size: int = -1
    """Log queue size, infinite by default"""

    batch_size: int = 50
    """Maximum number of log records to concatenate and write at once,
    consider setting it so an average batch would be ~ tens of KBs"""

    _write_queue: queue.Queue = field(default_factory=queue.Queue)
    _thread: Optional[Thread] = field(default=None)

    def __post_init__(self):
        self._levelno = _name_to_level[self._level]
        self._write_queue.maxsize = self.queue_size
        self._stream = None
        self._thread = None

    def handle(self, record: LogRecord, /) -> None:
        """Put a log record to the write queue."""
        if record.levelno < self._levelno:
            return
        if self._thread is None:
            self._thread = self._open_thread()
        self._write_queue.put(record)

    def _open_thread(self) -> Thread:
        self._write_queue.maxsize = self.queue_size
        thread = Thread(
            target=self.write_loop, name=f"{self} _write", args=(), daemon=True
        )
        thread.start()
        return thread

    def close(self) -> None:
        """Close the handler including all connections to its destination.

        This method is called automatically at exit for each added handler by the :py:func:`~uvlog.clear` function.
        """
        self._write_queue.put(self._sentinel)
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        # just in case the stream is not closed, however it should be closed when existing the `_write` method
        StreamHandler.close(self)

    def write_loop(self) -> None:
        """Write logs from the queue to the stream.

        This method is executed in a separate thread.
        """
        _queue = self._write_queue
        _queue.maxsize = self.queue_size
        _sentinel = self._sentinel
        _formatter = self._formatter
        _batch_size = self.batch_size
        self._stream = _stream = self._open_stream()
        formatted_records: List[bytes] = []
        while 1:
            if _queue.qsize():
                records = [_queue.get(block=True)]
            else:
                records = [
                    _queue.get_nowait() for _ in range(min(_batch_size, _queue.qsize()))
                ]
            for record in records:
                if record is _sentinel:
                    self.write(_stream, _queue, formatted_records)
                    StreamHandler.close(self)
                    return

                formatted_records.append(_formatter.format_record(record))

            self.write(_stream, _queue, formatted_records)
            formatted_records.clear()

    def write(
        self, _stream: BinaryIO, _queue: queue.Queue, formatted_records: List[bytes], /
    ) -> None:
        if not formatted_records:
            return
        try:
            formatted_records.append(b"")
            _stream.write(self.terminator.join(formatted_records))
        except Exception:  # noqa: acdceptable
            self._handle_error(formatted_records[0])
        finally:
            for _ in range(len(formatted_records) - 1):
                _queue.task_done()


def _merge_dicts(from_dict: dict, to_dict: dict) -> dict:
    _new_dict = {**from_dict}
    for key, value in to_dict.items():
        if key in _new_dict and type(value) is dict:
            _new_dict[key] = _merge_dicts(_new_dict[key], value)
        else:
            _new_dict[key] = value
    return _new_dict


def _configure_formatter(name: str, params: dict, /) -> None:
    cls = _formatter_types[params.pop("class", TextFormatter.__name__)]
    _formatter = cls()
    for key, value in params.items():
        if not key.startswith("_"):
            setattr(_formatter, key, value)
    _formatters[name] = _formatter


def _configure_handler(dest: str, params: dict, /) -> None:
    cls_name = params.pop("class", StreamHandler.__name__)
    _handler = _handler_types[cls_name]()
    _handler.set_destination(dest)
    formatter_name = params.pop("formatter", "text")
    _handler.set_formatter(_formatters[formatter_name])
    level: _LevelName = cast(_LevelName, params.pop("level", "DEBUG"))
    _handler.set_level(level)
    for key, value in params.items():
        if not key.startswith("_"):
            setattr(_handler, key, value)


def _configure_logger(name: str, params: dict, context_var: ContextVar, /) -> None:
    _logger = get_logger(name, persistent=True)
    handler_names = params.pop("handlers", [Stream.stderr.name])
    _logger.handlers = [_handlers[handler_name] for handler_name in handler_names]
    level: _LevelName = cast(_LevelName, params.pop("level", "INFO"))
    _logger.set_level(level)
    _logger.context = context_var
    for key, value in params.items():
        if not key.startswith("_"):
            setattr(_logger, key, value)


def configure(
    config_dict: _DictConfig, /, context_var: ContextVar = LOG_CONTEXT
) -> Logger:
    """Configure loggers for a configuration dict.

    :param config_dict: logging configuration (JSON compatible), at module init this function is called with
        `uvlog.BASIC_CONFIG` to provide default loggers and handlers
    :param context_var: log context variable, see `contextvars <https://docs.python.org/3/library/contextvars.html>`_

    This function is similar to dictConfig in the standard logging module, although the config format is slightly
    different.

    .. code-block:: python

        {
            "loggers": {
                "app": {
                    "level": "ERROR",
                    "handlers": ["my_file.txt"],
                    "capture_trace": True
                }
            },
            "handlers": {
                "my_file.txt": {
                    "class": "StreamHandler",
                    "level": "DEBUG",
                    "formatter": "my_format"
                }
            },
            "formatters": {
                "my_format": {
                    "class": "TextFormatter",
                    "format": "{name}: {message}"
                }
            }
        }

    The main differences are:

    - 'class' names for handlers and formatters must be registered beforehand using 'add_formatter_type()' and
        'add_handler_type()' respectively to allow classes not inherited from `Handler` / 'Formatter`
    - handler names are their destinations, since by design you're not allowed to bind multiple handlers to a single
        destination
    - 'format' for the text formatter should be in Python f-string format

    .. attention::

        The function is designed in such way you can extend or modify existing loggers, handlers or formatters
        by passing a config. If you want to configure logging from zero you should call `clear()` method beforehand.
        Please note that you need to provide all the handlers, formatters, loggers in the config after doing that,
        including the root logger (empty string).

    """
    clear()
    config_dict = cast(
        _DictConfig, _merge_dicts(cast(dict, BASIC_CONFIG), cast(dict, config_dict))
    )
    for name, params in config_dict["formatters"].items():
        _configure_formatter(name, params)
    for dest, params in config_dict["handlers"].items():
        _configure_handler(dest, params)
    # sorting loggers to init parents before children
    loggers_params = list(config_dict["loggers"].items())
    loggers_params.sort(key=lambda x: x[0])
    for name, params in loggers_params:
        _configure_logger(name, params, context_var)
    return _loggers[_root_logger_name]


def clear() -> None:
    """Clear all existing loggers, handlers and formatters.

    This function also closes all existing handlers.
    """
    _loggers_temp.clear()
    _loggers_persistent.clear()
    for handler in tuple(_handlers):
        remove_handler(handler)
    _formatters.clear()
