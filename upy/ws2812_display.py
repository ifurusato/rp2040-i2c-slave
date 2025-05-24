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

from plasma import WS2812
from motor import motor2040

from abstract_display import AbstractDisplay

class WS2812Display(AbstractDisplay):
    def __init__(self):
        self._led = WS2812(motor2040.NUM_LEDS, 1, 0, motor2040.LED_DATA)
        self._led.start()

    def show_color(self, color):
        self._led.set_rgb(0, color[0], color[1], color[2]) # RGB or GRB depending on LED type

#EOF
