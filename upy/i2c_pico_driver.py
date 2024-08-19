#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2024 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-18
# modified: 2024-08-19
#
# Extends I2CSlave as a driver file for the Raspberry Pi Pico RP2040, using
# its callback to print the message and set the LED on or off. This uses
# pin 16 for SDA and pin 17 for SCL.
#

from machine import Pin
from neopixel import Neopixel
from colors import COLOR_BLACK

from i2c_slave import I2CSlave

# ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
class I2CPicoDriver(I2CSlave):
    '''
    Wraps the functionality of the I2CSlave class with callback support for
    providing visual feedback via the green LED on the Raspberry Pi Pico.
    '''
    def __init__(self, i2c_address=0x44, blink=True):
        # Pico green LED on pin 25
        self._led = Pin(25, Pin.OUT)
        I2CSlave.__init__(self, i2c_address=i2c_address, sda=16, scl=17, blink=True, callback=self.callback)
        print('I2C pico driver ready.')

    def callback(self, message, color):
        if message:
            print('response: {}'.format(message))
        self.show_color(color)

    def show_color(self, color):
        '''
        Turns the LED on or off depending on if the argumeng is COLOR_BLACK or not.
        '''
        if color == COLOR_BLACK:
            self._led.off()
        else:
            self._led.on()

#EOF
