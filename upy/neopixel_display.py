#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-05-24
# modified: 2025-05-24

from machine import Pin
from neopixel import Neopixel
from abstract_display import AbstractDisplay

class NeopixelDisplay(AbstractDisplay):

    def __init__(self, num_leds=10, pin_num=17, brightness=108):
        self._neopixel = Neopixel(num_leds=num_leds, state_machine=0, pin=pin_num, mode="GRB")
        self._neopixel.brightness(brightness)
        Pin(16, Pin.OUT).value(1)

    def show_color(self, color):
        self._neopixel.set_pixel(0, color)
        self._neopixel.show()

#EOF
