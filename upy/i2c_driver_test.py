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
# Test file for I2CDriver that uses the callback to print the
# message and set the NeoPixel color.
#

from machine import Pin
from neopixel import Neopixel

from i2c_driver import I2CDriver

_driver = I2CDriver()
_driver.enable()

#EOF
