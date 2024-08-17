# This module is part of a substitute library for Colorama by Jonathan Hartley,
# and does nothing except return empty strings, since stdout in MicroPython is
# not implemented as it is in CPython.

def reset_all():
    pass

def init(autoreset=False, convert=None, strip=None, wrap=True):
    pass

def deinit():
    pass

def colorama_text(*args, **kwargs):
    pass

def reinit():
    pass

