#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2025 by Murray Altheim. All rights reserved. This file is part
# of the MR01 Robot Operating System (MROS) project, released under the MIT
# License. Please see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2020-01-14
# modified: 2025-05-24
#
# A simplified Logger, with no log to file, log suppression, heading or stats.

import os, logging, threading
from enum import Enum
from colorama import init, Fore, Style
init()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Level(Enum):
    DEBUG    = ( logging.DEBUG,    'DEBUG'    ) # 10
    INFO     = ( logging.INFO,     'INFO'     ) # 20
    WARN     = ( logging.WARN,     'WARN'     ) # 30
    ERROR    = ( logging.ERROR,    'ERROR'    ) # 40
    CRITICAL = ( logging.CRITICAL, 'CRITICAL' ) # 50

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    # ignore the first param since it's already set by __new__
    def __init__(self, num, label):
        self._label = label

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    @staticmethod
    def from_string(label):
        if label.upper()   == 'DEBUG':
            return Level.DEBUG
        elif label.upper() == 'INFO':
            return Level.INFO
        elif label.upper() == 'WARN':
            return Level.WARN
        elif label.upper() == 'ERROR':
            return Level.ERROR
        elif label.upper() == 'CRITICAL':
            return Level.CRITICAL
        else:
            raise NotImplementedError

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Logger:

    __color_debug    = Fore.BLUE   + Style.DIM
    __color_info     = Fore.CYAN   + Style.NORMAL
    __color_notice   = Fore.CYAN   + Style.BRIGHT
    __color_warning  = Fore.YELLOW + Style.NORMAL
    __color_error    = Fore.RED    + Style.NORMAL
    __color_critical = Fore.WHITE  + Style.NORMAL
    __color_reset    = Style.RESET_ALL

    def __init__(self, name, level=Level.INFO):
        '''
        Writes to a named log with the provided level, defaulting to a
        console (stream) handler unless 'log_to_file' is True, in which
        case only write to file, not to the console.

        :param name:           the name identified with the log output
        :param level:          the log level
        '''
        # configuration ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        _strip_ansi_codes       = True # used only with file output, to strip ANSI characters from log data
        self._include_timestamp = True
        self._date_format       = '%Y-%m-%dT%H:%M:%S'
#       self._date_format       = '%Y-%m-%dT%H:%M:%S.%f'
#       self._date_format       = '%H:%M:%S'
        # i18n?
        self.__DEBUG_TOKEN = 'DEBUG'
        self.__INFO_TOKEN  = 'INFO '
        self.__WARN_TOKEN  = 'WARN '
        self.__ERROR_TOKEN = 'ERROR'
        self.__FATAL_TOKEN = 'FATAL'
        self._mf           = '{}{} : {}{}'
        _1st_col_width     = 14

        # create logger  ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        self.__mutex = threading.Lock()
        self.__log   = logging.getLogger(name)
        self.__log.propagate = False
        self._name   = name
        self._sh     = None # stream handler
        if not self.__log.handlers:
            self._sh = logging.StreamHandler()
            if self._include_timestamp:
                self._sh.setFormatter(logging.Formatter(Fore.BLUE + Style.DIM + '%(asctime)s.%(msecs)3fZ\t:' \
                        + Fore.RESET + ' %(name)s ' + ( ' '*(_1st_col_width-len(name)) ) + ' : %(message)s', datefmt=self._date_format))
            else:
                self._sh.setFormatter(logging.Formatter('%(name)s ' + ( ' '*(_1st_col_width-len(name)) ) + ' : %(message)s'))
            self.__log.addHandler(self._sh)

        self.level = level

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
        orderly shutdown by flushing and closing all handlers. This should
        be called at application exit and no further use of the logging
        system should be made after this call.
        '''
        logging.shutdown()

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
        self.__log.setLevel(self._level.value)
        if self._sh:
            self._sh.setLevel(level.value)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def is_at_least(self, level):
        '''
        Returns True if the current log level is less than or equals the
        argument. E.g.,

            if self._log.is_at_least(Level.WARN):
                # returns True for WARN or ERROR or CRITICAL
        '''
        return self._level.value >= level.value

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def debug(self, message):
        '''
        Prints a debug message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        with self.__mutex:
            self.__log.debug(self._mf.format(Logger.__color_debug, self.__DEBUG_TOKEN, message, Logger.__color_reset))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def info(self, message):
        '''
        Prints an informational message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        with self.__mutex:
            self.__log.info(self._mf.format(Logger.__color_info, self.__INFO_TOKEN, message, Logger.__color_reset))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def notice(self, message):
        '''
        Functionally identical to info() except it prints the message brighter.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        with self.__mutex:
            self.__log.info(self._mf.format(Logger.__color_notice, self.__INFO_TOKEN, message, Logger.__color_reset))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def warning(self, message):
        '''
        Prints a warning message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        with self.__mutex:
            self.__log.warning(self._mf.format(Logger.__color_warning, self.__WARN_TOKEN, message, Logger.__color_reset))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def error(self, message):
        '''
        Prints an error message.

        The optional 'end' argument is for special circumstances where a different end-of-line is desired.
        '''
        with self.__mutex:
            self.__log.error(self._mf.format(Logger.__color_error, self.__ERROR_TOKEN, Style.NORMAL + message, Logger.__color_reset))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def critical(self, message):
        '''
        Prints a critical or otherwise application-fatal message.
        '''
        with self.__mutex:
            self.__log.critical(self._mf.format(Logger.__color_critical, self.__FATAL_TOKEN, Style.BRIGHT + message, Logger.__color_reset))

#EOF
