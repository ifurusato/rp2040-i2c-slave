#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020-2024 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-13
# modified: 2024-08-18
#
# A script that sends the command line argument as a packet to an I2C slave.
#
# see smbus2
# https://smbus2.readthedocs.io/en/latest/#smbus2.SMBus.write_block_data
#

import sys, traceback
from smbus import SMBus

from response import Response

if len(sys.argv) != 2:
    print("\nERROR: expected 1 command line argument: the data to transfer.")
    sys.exit(1)

_value = sys.argv[1]
print('-- value \"{}\"...'.format(_value))

# constants ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

I2C_SLAVE_ADDRESS = 0x44
CONFIG_REGISTER   = 1

# main ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

try:

    # convert source string to a list of bytes as a payload
    _payload = list(bytes(_value, 'utf-8'))
    if len(_payload) > 32:
        raise Exception('source text ({:d} chars) too long: 32 maximum.'.format(len(_payload)))

    print('creating connection to I2C bus on address 0x{:02X}…'.format(I2C_SLAVE_ADDRESS))
    _i2cbus = SMBus(1)  # create a new I2C bus

    print("writing I2C payload of {:d} chars: '{}'…".format(len(_value), _value))
    _i2cbus.write_block_data(I2C_SLAVE_ADDRESS, CONFIG_REGISTER, _payload)

    print('writing completion code…')
    _i2cbus.write_byte_data(I2C_SLAVE_ADDRESS, CONFIG_REGISTER, 0xff)

    print('write complete.')

    _read_data = _i2cbus.read_byte_data(I2C_SLAVE_ADDRESS, CONFIG_REGISTER)
    print("read data: '{}'".format(_read_data))
    _response = Response.from_value(_read_data)
    if _response is Response.OKAY:
        print("response: {}".format(_response.name))
    else:
        print("ERROR response: {}".format(_response.name))

except TimeoutError as te:
    print('ERROR: transfer timeout: {}'.format(te))
except Exception as e:
    print('ERROR: {} encountered: {}\n{}'.format(type(e), e, traceback.format_exc()))
finally:
    print('complete.')

#EOF
