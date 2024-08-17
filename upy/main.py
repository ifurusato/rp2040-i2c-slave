#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2024 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-14
# modified: 2024-08-18
#
# This is a script for using the ItsyBitsy RP2040 as an I2C slave device, using
# the NeoPixel as a status indicator. Configuration is pin 24 for SDA, pin 25
# for SCL. This can be modified to suit a different RP2040 board.
#
# The receive mode permits strings of up to 32 characters, composed of ASCII
# characters between SPACE (20) and '~' (126).
#
# This returns a response code in the form of a single byte.
#

import machine
import utime
from machine import Pin
from neopixel import Neopixel
from RP2040_Slave import i2c_slave

import itertools
from colors import*
from stringbuilder import StringBuilder

# constants ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

I2C_ID            = 0
SDA_PIN           = 24
SCL_PIN           = 25
I2C_ADDRESS       = 0x44
MAX_CHARS         = 32

# response codes:
INIT              = 0x10
OKAY              = 0x20
BAD_ADDRESS       = 0x41
OUT_OF_SYNC       = 0x42
INVALID_CHAR      = 0x43
SOURCE_TOO_LARGE  = 0x44
UNVALIDATED       = 0x45
EMPTY_PAYLOAD     = 0x46
PAYLOAD_TOO_LARGE = 0x47
UNKNOWN_ERROR     = 0x48

# variables ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

# NeoPixel control pin 17
_neopixel = Neopixel(num_leds=10, state_machine=0, pin=17, mode="RGB")
_neopixel.brightness(108)
# turn on NeoPixel power pin 16
_pin16 = Pin(16, Pin.OUT)
_pin16.value(1)

_tx_counter = itertools.count()
_counter = itertools.count()

# establish I2C slave ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
print("starting I2C slave…")
s_i2c = i2c_slave(I2C_ID, sda=SDA_PIN, scl=SCL_PIN, slaveAddress=I2C_ADDRESS)

# initial conditions ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
index = 0
payload = ''
response = INIT
currentTransaction = s_i2c.I2CTransaction(0x00, [])
state = s_i2c.I2CStateMachine.I2C_START

# classes ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

class I2CSlaveError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self._code = code

    @property
    def code(self):
        return self._code

# methods ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

def show_color(color):
    '''
    Display the color on the NeoPixel.
    '''
    _neopixel.set_pixel(0, color)
    _neopixel.show()

def process_buffer(buffer):
    '''
    Receives the packet sent by the master, returning the contents as a string.
    This can be expanded to further process the value.
    '''
    __payload = buffer.to_string()
    print("received payload: '{}'".format(__payload))
    return __payload

def reset():
    index = 0
    payload = ''
    response = INIT
    currentTransaction.reset()
    state = s_i2c.I2CStateMachine.I2C_START

# main ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

# indicate startup…
for i in range(3):
    show_color(COLOR_CYAN)
    utime.sleep_ms(50)
    show_color(COLOR_BLACK)
    utime.sleep_ms(50)
utime.sleep_ms(333)

print("starting loop…")

while True:
    try:
        state = s_i2c.handle_event()
        if state == None:
            pass
        elif state == s_i2c.I2CStateMachine.I2C_START:
            show_color(COLOR_MAGENTA)
        elif state == s_i2c.I2CStateMachine.I2C_RECEIVE:
            show_color(COLOR_YELLOW)
            '''
            Receive data from the master. The first byte is 0x00, followed by a byte
            indicating the count of bytes in the payload, then the data bytes followed
            by 0x01 to validate, then 0xff to finish.
            '''
            if currentTransaction.address == 0x00:
                # first byte received is the register address
                _register_address = s_i2c.Read_Data_Received()
                currentTransaction.address = _register_address

            _valid = False
            index = 0
            _sb = StringBuilder()
            _expected_length = 0

            # read all data byte received until Rx FIFO is empty
            while s_i2c.Available():
                _data_rx = s_i2c.Read_Data_Received()
                _int_value = int(_data_rx)
                if _data_rx == 0x00:
                    pass
                elif _data_rx == 0x01:
                    _valid = True
                elif _data_rx == 0xFF:
                    show_color(COLOR_MAGENTA)
                    break
                else:
                    if index == 0:
                        _expected_length = _int_value
                        if _expected_length > MAX_CHARS:
                            show_color(COLOR_ORANGE)
                            raise I2CSlaveError(SOURCE_TOO_LARGE, "WARNING: packet failed with {:d} chars, exceeded maximum length of {:d}.".format(_expected_length, MAX_CHARS))
                    elif _sb.length() < _expected_length:
                        if ( _int_value >= 32 ) and ( _int_value < 127 ):
                            _sb.append(chr(_data_rx))
                        else:
                            show_color(COLOR_RED)
                            raise I2CSlaveError(INVALID_CHAR, "invalid character received: '0x{:02X}' (int: '{:d}'); buf length: {:d}; sb: '{}'".format(_data_rx, _int_value, _sb.length(), _sb.to_string()))
                    else:
                        show_color(COLOR_RED)
                        raise I2CSlaveError(OUT_OF_SYNC, "out of sync: '0x{:02X}' (int: '{:d}'); buf length: {:d}; sb: '{}'".format(_data_rx, _int_value, _sb.length(), _sb.to_string()))
                index = index + 1
                currentTransaction.data_byte.append(_data_rx)

            if _sb.length() > 0:
                if _valid:
                    if _expected_length != _sb.length():
                        show_color(COLOR_RED)
                        raise I2CSlaveError(PAYLOAD_TOO_LARGE, "package failed with expected length: {:d}; actual length: {:d}.".format(_expected_length, _sb.length()))
                    else:
                        payload = process_buffer(_sb)
                else:
                    show_color(COLOR_RED)
                    raise I2CSlaveError(UNVALIDATED, "unvalidated buffer: '{}'".format(_sb.to_string()))

            # end of receive loop
            show_color(COLOR_GREEN)

        elif state == s_i2c.I2CStateMachine.I2C_REQUEST:
            if len(payload) > 0:
                show_color(COLOR_GREEN)
                response = OKAY
            else:
                show_color(COLOR_RED)
                response = EMPTY_PAYLOAD
            # otherwise use existing response
            while (s_i2c.is_Master_Req_Read()):
                s_i2c.Slave_Write_Data(response)

        elif state == s_i2c.I2CStateMachine.I2C_FINISH:
            show_color(COLOR_BLUE)
            reset()

        # now blink
        if next(_counter) % 1000 == 0:
            show_color(COLOR_DARK_CYAN)
            utime.sleep_ms(4)
            show_color(COLOR_BLACK)

    except KeyboardInterrupt:
        break
    except I2CSlaveError as se:
        print('I2C slave error {} on transaction: {}'.format(se.code, str(se)))
        # empty buffer
        while s_i2c.Available():
            _data_rx = s_i2c.Read_Data_Received()
        reset()
        while (s_i2c.is_Master_Req_Read()):
            print("sending error response: {}".format(str(se)))
            s_i2c.Slave_Write_Data(se.code)
    except Exception as e:
        print('Exception raised: {}'.format(e))

#EOF
