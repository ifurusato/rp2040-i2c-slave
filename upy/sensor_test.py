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
# This is a test script for the Sensor class, which extends I2CDriver to
# return the value of a generic GPIO pin-based sensor. The enumerated
# set of single byte response codes is likewise extended to return new
# values suitable to the sensor ("on" or "off").
#

import sys
import utime
from sensor import Sensor

# main ................................

try:

    _sensor = Sensor(18)
    _sensor.enable()

    while True:
        utime.sleep(3)

except KeyboardInterrupt:
    print('Ctrl-C caught, exiting…')
    sys.exit(0)

#EOF
