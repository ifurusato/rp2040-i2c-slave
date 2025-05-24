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
from machine import Timer
import uasyncio as asyncio
from colorama import Fore, Style

from colors import*
from core.logger import Level, Logger
from payload import Payload
from response import*

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Controller:
    '''
    A generalised controller for hardware connected to the RP2040.

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
        This doesn't currently do anything.
        '''
        self._enabled = True
        self._log.info('enabled.')
        self.show_color(COLOR_CYAN)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def disable(self):
        '''
        Sets the Controller's enabled flag to False.
        This doesn't currently do anything.
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
            self._display.show_color(color)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def process_payload(self, payload):
        '''
        Immediately returns and delegates payload processing to an async task.
        '''
        if not isinstance(payload, Payload):
            raise ValueError('expected Payload not {}'.format(type(payload)))
        if self._processing_task is None:
            self._processing_task = asyncio.create_task(self._async_process_payload(payload))
            self._log.info('task created.')
            # ensure the event loop is running
            asyncio.get_event_loop().run_forever() # keep the event loop running
            self._log.info(Style.DIM + 'payload processing complete.')
            return RESPONSE_OKAY
        elif self._processing_task.done():
            self._processing_task = None
            return RESPONSE_OUT_OF_SYNC
        else:
            self._log.warning("another task is already running, skipping new payload.")
            return RESPONSE_BUSY

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    async def _async_process_payload(self, payload):
        '''
        Async payload processor.
        '''
        self._log.info("process payload '{}'…".format(payload.to_string()))
        try:
            self.show_color(COLOR_SKY_BLUE)
            _command = payload.command
            self._log.info("payload: " + Fore.GREEN + "'{}'".format(_command))
            if _command == 'help':
                self.help()
            elif _command.startswith('enab'):
                self.enable()
            elif _command.startswith('disa'):
                self.disable()
            elif _command.startswith('start'):
                self.start()
            elif _command.startswith('stop'):
                self.stop()
            elif _command.startswith('red'):
                self.show_color(COLOR_RED)
            elif _command == 'green':
                self.show_color(COLOR_GREEN)
            elif _command == 'blue':
                self.show_color(COLOR_BLUE)
            elif _command == 'black':
                self.show_color(COLOR_BLACK)
            elif _command.startswith('wait'):
                self.show_color(COLOR_VIOLET)
                _duration = self._parse_duration(_command, default=5)
                self._log.info("waiting for {:.2f} seconds.".format(_duration))
                await asyncio.sleep(_duration)
                self.show_color(COLOR_DARK_VIOLET)
            else:
                self._log.warning("unknown command: '{}'".format(_command))
                self.show_color(COLOR_ORANGE)
        except Exception as e:
            self._log.error("error processing command: {}".format(e))
            sys.print_exception(e)
            self.show_color(COLOR_RED)
            return RESPONSE_UNKNOWN_ERROR
        finally:
            self._processing_task = None

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _parse_duration(self, arg, default=5):
        try:
            rest = arg[4:].strip()
            return int(rest)
        except ValueError:
            pass
        return default

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def start(self):
        self._log.info('start.')
        self._start_timer();
 
    def _start_timer(self):
        if not self._timer:
            self._timer = Timer()
            self._timer.init(period=1000, mode=Timer.PERIODIC, callback=self._toggle_led)

    def _toggle_led(self, arg):
        self._on = not self._on
        if self._on:
            self.show_color(COLOR_DARK_CYAN)
            utime.sleep_ms(50)
            self.show_color(COLOR_BLACK)
        else:
            pass

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def stop(self):
        self._log.info('stop.')
        self._stop_timer();

    def _stop_timer(self):
        if self._timer:
            self._timer.deinit()
        self._timer = None

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def help(self):
        print(Fore.CYAN + '''
controller commands:
    
    enable            enable controller
    disable           disable and exit the controller
    red               set the RGB LED to red
    green             set the RGB LED to green
    blue              set the RGB LED to blue
    black             set the RGB LED to black (off)
    start             start a timer that blinks the LED
    stop              stop the timer
    wait [n]          asynchronously wait n seconds (default 5)

    ''' + Style.RESET_ALL)

#EOF
