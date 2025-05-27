#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-14
# modified: 2025-05-24
#
# Starts an I2C slave with a Controller handler for incoming payloads.
# Note that the SDA and SCL pins are the same on Pico and ItsyBitsy RP2040,
# i.e., SDA = 2, SCL = 3.

import sys
import utime

from core.logger import Level, Logger
from colors import*
from colorama import Fore, Style
from i2c_slave import I2CSlave
#from controller import Controller
from motor_controller import MotorController
from payload import Payload
from response import*

# constants ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

I2C_BUS_ID    = 1
SDA_PIN       = 2
SCL_PIN       = 3
I2C_ADDRESS   = 0x43
DISPLAY_TYPE  = 'neopixel' # | 'ws2812' | 'pico'
START_COUNT   = 3

# init ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

_log = Logger('main', Level.INFO)
_log.info(Fore.WHITE + "initialising…")

# functions ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

def get_display(name="neopixel"):
    if name == "neopixel":
        from neopixel_display import NeopixelDisplay
        return NeopixelDisplay()
    elif name == "ws2812":
        from ws2812_display import WS2812Display
        return WS2812Display()
    elif name == "pico":
        from pico_display import PicoDisplay
        return PicoDisplay()
    else:
        raise ValueError("unrecognised display type: {}".format(DISPLAY_TYPE))

def show_color(color):
    '''
    Display the color on the NeoPixel.
    '''
    _log.debug(Style.DIM + "show color: {}".format(color.description))
    display.show_color(color)

# main ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

# indicate startup, waiting 5 seconds so it can be interrupted…

display = get_display(DISPLAY_TYPE)

for i in range(START_COUNT):
    show_color(COLOR_CYAN)
    utime.sleep_ms(50)
    show_color(COLOR_BLACK)
    _log.info(Style.DIM + '[{}/{}] starting…'.format(i, START_COUNT))
    utime.sleep_ms(950)
utime.sleep_ms(50)

i2c_slave = None
try:
    _name = '0x{:02X}'.format(I2C_ADDRESS) # or some more meaningful name
    _log.info('start I2C slave…')
    _controller = MotorController(display)
    i2c_slave = I2CSlave(name=_name, i2c_bus_id=I2C_BUS_ID, sda=SDA_PIN, scl=SCL_PIN, i2c_address=I2C_ADDRESS, display=display, controller=_controller)
    _controller.start()
    i2c_slave.enable()
    _log.warning('I2C slave started; it should have blocked.')
except KeyboardInterrupt:
    _log.info('Ctrl-C caught; exiting…')
except Exception as e:
    _log.error('{} raised in main loop: {}'.format(type(e), e))
    sys.print_exception(e)
finally:
    if i2c_slave:
        i2c_slave.disable()

# this only happens following an 'exit', which also disables the I2C slave
_log.info('exit: loop complete.')
show_color(COLOR_DARK_RED)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class I2CSlaveError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self._code = code

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    @property
    def code(self):
        return self._code

#EOF
