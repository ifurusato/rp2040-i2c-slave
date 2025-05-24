#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2025 by Murray Altheim. All rights reserved. This file is part
# of the MR01 Robot Operating System (MROS) project, released under the MIT
# License. Please see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2020-01-14
# modified: 2025-04-26

# this is a simplification of the MROS Logger class, just using print statements
# and not supporting log-to-file, log suppression, the notice() or critical()
# levels, etc.
#

import math
import time
from colorama import Fore, Style

def enum(**enums: int):
    return type('Enum', (), enums)

Level = enum(DEBUG=10, INFO=20, WARN=30, ERROR=40)
# e.g., levels = (Level.ONE, Level.TWO)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Logger:

    __color_debug    = Fore.BLUE   + Style.DIM
    __color_info     = Fore.CYAN   + Style.NORMAL
    __color_warning  = Fore.YELLOW + Style.NORMAL
    __color_error    = Fore.RED    + Style.NORMAL
    __color_reset    = Style.RESET_ALL

    def __init__(self, name, level=Level.INFO):
        '''
        Writes to the console with the provided level.

        :param name:     the name identified with the log output
    :param level:    the log level
    '''
        # configuration ..........................
        self._include_timestamp = True
        self.__DEBUG_TOKEN = 'DEBUG'
        self.__INFO_TOKEN  = 'INFO '
        self.__WARN_TOKEN  = 'WARN '
        self.__ERROR_TOKEN = 'ERROR'
        self.__FATAL_TOKEN = 'FATAL'
        self._name_format  = '{:<14} : '
        # during sync (e.g., after NTP sync)
        self._boot_time = time.time()  # seconds since epoch
        self._boot_ticks = time.ticks_ms()
        self._name   = name
        self.level = level

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _get_timestamp(self):
        while True:
            ticks1 = time.ticks_ms()
            t = time.localtime()
            ticks2 = time.ticks_ms()
            if ticks1 // 1000 == ticks2 // 1000:
                ms = ticks1 % 1000
                return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:03d}Z".format(
                    t[0], t[1], t[2], t[3], t[4], t[5], ms
                )

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _get_time(self):
        return self._get_timestamp()

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    @property
    def name(self):
        '''
        Return the name of this Logger.
        '''
        return self._name

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def close(self):
        '''
        Closes down logging, and informs the logging system to perform an
        orderly shutdown by flushing and closing all handlers.

        This is not supported in this implementation, but raises no exception
        when called.
        '''
        pass

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    @property
    def level(self):
        '''
        Return the level of this logger.
        '''
        return self._level

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    @level.setter
    def level(self, level):
        '''
        Set the level of this logger to the argument.
        '''
        self._level = level

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def is_at_least(self, level):
        '''
        Returns True if the current log level is less than or equals the
        argument. E.g.,

            if self._log.is_at_least(Level.WARN):
                # returns True for WARN or ERROR or CRITICAL
        '''
        return level >= self._level

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def debug(self, message):
        '''
        Prints a debug message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        if self.is_at_least(Level.DEBUG):
            timestamp = self._get_time()
            print(Fore.BLUE + "{} : ".format(timestamp) 
                    + Style.DIM + Fore.RESET
                    + self._name_format.format(self._name)
                    + Logger.__color_debug + "{} : ".format(self.__DEBUG_TOKEN)
                    + Fore.CYAN + "{}".format(message) + Logger.__color_reset)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def info(self, message):
        '''
        Prints an informational message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        if self.is_at_least(Level.INFO):
            timestamp = self._get_time()
            print(Fore.BLUE + "{} : ".format(timestamp) 
                    + Style.DIM + Fore.RESET
                    + self._name_format.format(self._name)
                    + Logger.__color_info + "{} : ".format(self.__INFO_TOKEN)
                    + Fore.CYAN + "{}".format(message) + Logger.__color_reset)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def warning(self, message):
        '''
        Prints a warning message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        if self.is_at_least(Level.WARN):
            timestamp = self._get_time()
            print(Fore.BLUE + "{} : ".format(timestamp)
                    + Style.DIM + Fore.RESET
                    + self._name_format.format(self._name)
                    + Logger.__color_warning + "{} : ".format(self.__WARN_TOKEN)
                    + Fore.CYAN + "{}".format(message) + Logger.__color_reset)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def error(self, message):
        '''
        Prints an error message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        if self.is_at_least(Level.ERROR):
            timestamp = self._get_time()
            print(Fore.BLUE + "{} : ".format(timestamp) 
                    + Style.DIM + Fore.RESET
                    + self._name_format.format(self._name)
                    + Logger.__color_error + "{} : ".format(self.__ERROR_TOKEN)
                    + Fore.CYAN + "{}".format(message) + Logger.__color_reset)

#EOF
