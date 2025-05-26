#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-05-25
# modified: 2025-05-25
#

import sys
import utime
from machine import Timer
import uasyncio as asyncio
from colorama import Fore, Style

from colors import*
from core.logger import Level, Logger
from controller import Controller
from response import*

class MotorController(Controller):
    '''
    Extends Controller with motor-specific and some other demonstration commands.
    '''
    def __init__(self, display=None, level=Level.INFO):
        super().__init__(display=display, level=level)
        self._log = Logger('motor', level)
        self._motor_speed = 0
        self._motor_enabled = False
        self._log.info('ready.')

    async def handle_command(self, command):
        '''
        Extended async processor for motor-specific commands.
        '''
#       self._log.debug("handling command: '{}'".format(command))
        try:
            if command.startswith('help'):
                self.help()

            # fake motor control ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
            elif command.startswith('motor-on'):
                self.motor_on()
            elif command.startswith('motor-off'):
                self.motor_off()
            elif command.startswith('motor-speed'):
                speed = self._parse_motor_speed(command)
                self.set_motor_speed(speed)

            # set some colors ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
            elif command == 'red':
                self.show_color(COLOR_RED)
            elif command == 'green':
                self.show_color(COLOR_GREEN)
            elif command == 'blue':
                self.show_color(COLOR_BLUE)
            elif command == 'black':
                self.show_color(COLOR_BLACK)

            # start and stop a timer ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
            elif command == 'start':
                self.start()
            elif command == 'stop':
                self.stop()

            # asynchronous wait ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
            elif command.startswith('wait'):
                self.show_color(COLOR_VIOLET)
                _duration = self._parse_duration(command, default=5)
                self._log.info("waiting for {:.2f} seconds.".format(_duration))
                await asyncio.sleep(_duration)
                self.show_color(COLOR_DARK_VIOLET)
            else:
                # delegate to base class if not processed ┈┈┈┈┈┈┈┈┈┈┈┈
                await super().handle_command(command)

        except Exception as e:
            self._log.error("MotorController error: {}".format(e))
            sys.print_exception(e)
            self.show_color(COLOR_RED)
            return RESPONSE_UNKNOWN_ERROR
        finally:
            self._processing_task = None

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _parse_duration(self, arg, default=5):
        try:
            parts = arg.strip().split()
            if len(parts) >= 2:
                return int(parts[1])
        except ValueError:
            pass
        return default

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def validated(self):
#       self._log.debug("validated.")
        if self._timer:
            self.stop()
        super().validated()

    # help ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def help(self):
        print(Fore.CYAN + '''
motor controller commands:

    help              prints this help
    enable            enable controller
    disable           disable and exit the controller
    motor-on          turn on the fake motor
    motor-off         turn off the fake motor
    motor-speed [n]   set the motor speed to n
    start             start a timer that blinks the LED
    stop              stop the timer
    red               set the RGB LED to red
    green             set the RGB LED to green
    blue              set the RGB LED to blue
    black             set the RGB LED to black (off)
    wait [n]          asynchronously wait n seconds (default 5)

    ''' + Style.RESET_ALL)

    # fake motor control ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

    def motor_on(self):
        self._log.info("turning motor ON")
        # Add logic to enable motor hardware

    def motor_off(self):
        self._log.info("turning motor OFF")
        # Add logic to disable motor hardware

    def set_motor_speed(self, speed):
        self._log.info("setting motor speed to {}".format(speed))
        # Add logic to set motor speed

    def _parse_motor_speed(self, command, default=50):
        '''
        Parse the last token in the command as an int. If there is
        no value or a parsing error occurs, returns the default value.

        e.g., command is like "motor-speed 100"
        '''
        try:
            parts = command.split()
            return int(parts[-1])
        except (IndexError, ValueError):
            self._log.warning("failed to parse motor speed, using default of {}".format(default))
            return default

    # start and stop a timer ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def start(self):
        if not self._timer:
            self._log.info('timer: ' + Fore.GREEN + 'start')
            self._timer = Timer()
            self._timer.init(period=1000, mode=Timer.PERIODIC, callback=self._toggle_led)
        else:
            self._log.warning('timer already started.')

    def _toggle_led(self, arg):
        self._on = not self._on
        if self._on:
            self.show_color(COLOR_DARK_CYAN)
            utime.sleep_ms(50)
            self.show_color(COLOR_BLACK)
        else:
            pass

    def stop(self):
        if self._timer:
            self._log.info('timer: ' + Fore.GREEN + 'stop')
            self._timer.deinit()
        else:
            self._log.warning('timer already stopped.')
        self._timer = None

#EOF
