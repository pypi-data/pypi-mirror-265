"""Python logging utilities."""

import atexit

from uvlog.uvlog import *

__python_version__ = "3.8"
__author__ = "violetblackdev@gmail.com"
__license__ = "MIT"
__version__ = "0.1.1"

add_formatter_type(TextFormatter)
add_formatter_type(JSONFormatter)
add_handler_type(StreamHandler)
add_handler_type(QueueHandler)
configure(BASIC_CONFIG)
atexit.register(clear)
