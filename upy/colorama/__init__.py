# This module is part of a substitute library for Colorama by Jonathan Hartley,
# and does nothing except return empty strings, since stdout in MicroPython is
# not implemented as it is in CPython.

from .initialise import init, deinit, reinit, colorama_text
from .ansi import Fore, Back, Style, Cursor

__version__ = '0.4.4'
