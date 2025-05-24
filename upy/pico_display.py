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

from abstract_display import AbstractDisplay

class PicoDisplay(AbstractDisplay):
    def __init__(self):
        self._led = Pin(25, Pin.OUT)

    def show_color(self, color):
        self._led.value(0 if color == (0, 0, 0) else 1)

#EOF
