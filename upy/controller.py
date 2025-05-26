#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-04-25
# modified: 2025-05-24
#

import sys
import utime
import uasyncio as asyncio
from colorama import Fore, Style

from colors import*
from core.logger import Level, Logger
from payload import Payload
from response import*

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Controller:
    '''
    A minimal, generalised controller for hardware connected to the RP2040.
    This is meant to be subclassed with commands tailored for specific
    applications.

    :param display:   the optional display (e.g., RGB LED)
    :param level:     the log level
    '''
    def __init__(self, display=None, level=Level.INFO):
        self._log = Logger('controller', level)
        self._display = display
        self._processing_task = None
        self._enabled = False
        self._timer   = None
        self._on      = False
        self._log.info('ready.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    @property
    def enabled(self):
        '''
        Returns the Controller's enabled flag as a property.
        '''
        return self._enabled

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def enable(self):
        '''
        Sets the Controller's enabled flag to True.
        '''
        self._enabled = True
        self._log.info('enabled.')
        self.show_color(COLOR_CYAN)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def disable(self):
        '''
        Sets the Controller's enabled flag to False.
        '''
        self._enabled = False
        self._log.info('disabled.')
        self.show_color(COLOR_DARK_GREY)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def show_color(self, color):
        '''
        Display the color on the display device.
        '''
        if self._display:
            self._log.debug(Style.DIM + 'show color: {}'.format(color.description))
            self._display.show_color(color)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def process_payload(self, payload):
        '''
        Immediately returns and delegates payload processing to an async task.
        '''
        if not isinstance(payload, Payload):
            raise ValueError('expected Payload not {}'.format(type(payload)))
        if self._processing_task is None:
            self._processing_task = asyncio.create_task(self.handle_command(payload.command))
            self._log.debug('task created.')
            # ensure the event loop is running
            asyncio.get_event_loop().run_forever() # keep the event loop running
#           self._log.debug('payload processing complete.')
            return RESPONSE_OKAY
        elif self._processing_task.done():
            self._processing_task = None
            return RESPONSE_OUT_OF_SYNC
        else:
            self._log.warning("another task is already running, skipping new payload.")
            return RESPONSE_BUSY

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    async def handle_command(self, command):
        '''
        Async payload processor. This understands 'help', 'enable' and 'disable',
        and is meant to be overridden by subclasses.
        '''
#       self._log.debug("handling command: " + Fore.GREEN + "'{}'".format(command))
        try:
            self.show_color(COLOR_SKY_BLUE)
            if command == 'help':
                self.help()
            elif command.startswith('enab'):
                self.enable()
            elif command.startswith('disa'):
                self.disable()
            else:
                self._log.warning("unknown command: '{}'".format(command))
                self.show_color(COLOR_ORANGE)
        except Exception as e:
            self._log.error("error processing command: {}".format(e))
            sys.print_exception(e)
            self.show_color(COLOR_RED)
            return RESPONSE_UNKNOWN_ERROR
        finally:
            self._processing_task = None

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def validated(self):
        '''
        This is called upon validating a payload has been successfully received.
        '''
#       self._log.debug("validated.")
        pass

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def help(self):
        print(Fore.CYAN + '''
controller commands:

    help              prints this help
    enable            enable controller
    disable           disable and exit the controller

    ''' + Style.RESET_ALL)

#EOF
