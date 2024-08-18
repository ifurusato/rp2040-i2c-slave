#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2024 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-18
# modified: 2024-08-18
#
# Extends I2CSlave as a driver file for the Adafruit ItsyBitsy RP2040, using
# its callback to print the message and set the NeoPixel color.
#

from machine import Pin
from neopixel import Neopixel

from i2c_slave import I2CSlave

# ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
class I2CDriver(I2CSlave):
    '''
    Wraps the functionality of the I2CSlave class with callback support
    for providing visual feedback via a NeoPixel, as found on the Adafruit
    ItsyBitsy RP2040.
    '''
    def __init__(self, i2c_address=0x44, blink=True):
        # NeoPixel control pin 17
        self._neopixel = Neopixel(num_leds=10, state_machine=0, pin=17, mode="RGB")
        self._neopixel.brightness(108)
        # turn on NeoPixel power pin 16
        _pin16 = Pin(16, Pin.OUT)
        _pin16.value(1)
        I2CSlave.__init__(self, i2c_address=i2c_address, blink=blink, callback=self.callback)
        print('I2C driver ready.')

    def callback(self, message, color):
        if message:
            print('response: {}'.format(message))
        self.show_color(color)

    def show_color(self, color):
        '''
        Display the color on the NeoPixel.
        '''
        self._neopixel.set_pixel(0, color)
        self._neopixel.show()

#EOF
