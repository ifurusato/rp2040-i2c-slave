# This module is part of a substitute library for Colorama by Jonathan Hartley,
# and does nothing except return empty strings, since stdout in MicroPython is
# not implemented as it is in CPython.


class AnsiCodes(object):
    def __init__(self):
        pass

class AnsiCursor(object):
    def UP(self, n=1):
        return ''
    def DOWN(self, n=1):
        return ''
    def FORWARD(self, n=1):
        return ''
    def BACK(self, n=1):
        return ''
    def POS(self, x=1, y=1):
        return ''

class AnsiFore():
    BLACK           = ''
    RED             = ''
    GREEN           = ''
    YELLOW          = ''
    BLUE            = ''
    MAGENTA         = ''
    CYAN            = ''
    WHITE           = ''
    RESET           = ''
    LIGHTBLACK_EX   = ''
    LIGHTRED_EX     = ''
    LIGHTGREEN_EX   = ''
    LIGHTYELLOW_EX  = ''
    LIGHTBLUE_EX    = ''
    LIGHTMAGENTA_EX = ''
    LIGHTCYAN_EX    = ''
    LIGHTWHITE_EX   = ''


class AnsiBack(AnsiCodes):
    BLACK           = ''
    RED             = ''
    GREEN           = ''
    YELLOW          = ''
    BLUE            = ''
    MAGENTA         = ''
    CYAN            = ''
    WHITE           = ''
    RESET           = ''
    LIGHTBLACK_EX   = ''
    LIGHTRED_EX     = ''
    LIGHTGREEN_EX   = ''
    LIGHTYELLOW_EX  = ''
    LIGHTBLUE_EX    = ''
    LIGHTMAGENTA_EX = ''
    LIGHTCYAN_EX    = ''
    LIGHTWHITE_EX   = ''


class AnsiStyle(AnsiCodes):
    BRIGHT    = ''
    DIM       = ''
    NORMAL    = ''
    RESET_ALL = ''

Fore   = AnsiFore()
Back   = AnsiBack()
Style  = AnsiStyle()
Cursor = AnsiCursor()
