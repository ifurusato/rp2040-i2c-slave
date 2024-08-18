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
# An example class that extends I2CDriver (which extends I2CSlave),
# to return the value of a generic GPIO pin-based sensor.
#

import utime
from machine import Pin
from i2c_driver import I2CDriver

class Sensor(I2CDriver):
    # additional response codes (< 0x4F):
    OFF = 0x30
    ON  = 0x31
    '''
    A simple class to read the value of a GPIO pin.
    '''
    def __init__(self, pin=18):
        I2CDriver.__init__(self)
        self._pin = Pin(18, Pin.IN)

    @property
    def on(self):
        '''
        Returns True when the pin is low.
        '''
        return not self._pin.value()

    def callback(self, message, color):
        if message:
            print('sensor response: {}'.format(message))
#       self.show_color(color)
        I2CDriver.callback(self, message, color)

    def write_response(self, response):
        '''
        Writes the single byte response to the I2C bus.
        If the value is less than OKAY (0x4F) the returned
        value is set by the sensor as 'OFF' or 'ON'
        '''
        if response <= I2CDriver.OKAY:
            if self.on:
                I2CDriver.write_response(self, self.ON)
            else:
                I2CDriver.write_response(self, self.OFF)
        else:
            I2CDriver.write_response(self, response)

#EOF
