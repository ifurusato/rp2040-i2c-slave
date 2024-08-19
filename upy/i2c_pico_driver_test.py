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
# Test file for I2CPicoDriver that uses the callback to print the
# message and set the Raspberry Pi Pico's LED.
#

from i2c_pico_driver import I2CPicoDriver

_driver = I2CPicoDriver()
_driver.enable()

#EOF
