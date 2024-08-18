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
# Test file for I2CSlave. This starts the I2CSlave loop without any support
# for a NeoPixel.
#

from i2c_slave import I2CSlave

_i2c_slave = I2CSlave()
_i2c_slave.enable()

#EOF
