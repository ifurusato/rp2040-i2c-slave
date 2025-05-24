#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-13
# modified: 2025-05-24
#

import traceback
from smbus import SMBus
import datetime as dt
from colorama import init, Fore, Style
init()

from core.logger import Logger, Level
from core.payload import Payload 
from core.response import*

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Controller:
    '''
    A generalised controller connected to an I2C slave.

    No argument defaults.
    :param i2c_bus:       the I2C bus ID (0 or 1)
    :param i2c_address:   the I2C address
    :param level:         the logging level
    '''
    def __init__(self, i2c_bus=None, i2c_address=None, level=Level.INFO):
        self._log = Logger('controller', level)
        self._i2c_address = i2c_address
        self._config_register = 1
        try:
            self._i2cbus = SMBus(i2c_bus)
        except Exception as e:
            self._log.error('{} raised, could not connect to I2C bus: {}'.format(type(e), e))
            self._i2cbus = None
        self._last_payload      = None
        self._last_send_time = None  # timestamp of last send
        self._min_send_interval = dt.timedelta(milliseconds=70) # 70ms
        self._log.info('ready.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def send_payload(self, command):
        '''
        Generates a payload and sends it to the I2C slave.

        If a previous payload exists and the arguments are withing tolerance of
        it, the method exits, doing nothing.
        '''
        if self._last_payload is not None:
            if self._last_payload.command == command:
                self._log.info(Fore.BLUE + 'NOT sending redundant payload: {}'.format(self._last_payload))
                return RESPONSE_SKIPPED
        self._log.info("send payload: " + Fore.GREEN + "'{}'".format(command))
        _payload = Payload(command)
        return self._write_payload(_payload)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _write_payload(self, payload, verbose=True):
        '''
        Writes the payload argument to the Motor 2040.
        '''
        if self._last_payload is not None and self._last_payload == payload:
            self._log.info(Fore.BLUE + 'b. NOT sending redundant payload: {}'.format(self._last_payload))
            return RESPONSE_SKIPPED
        self._last_payload = payload
        now = dt.datetime.now()
        if self._last_send_time:
            elapsed = now - self._last_send_time
            if elapsed < self._min_send_interval:
                self._log.warning(
                    "write_payload skipped: only {:.1f}ms since last send (minimum is {:.1f}ms)".format(
                        elapsed.total_seconds() * 1000,
                        self._min_send_interval.total_seconds() * 1000
                    )
                )
                return RESPONSE_SKIPPED
        try:
            if verbose:
                self._log.debug("writing payload: " + Fore.WHITE + "'{}'".format(payload.to_string()))
            # send over I2C
            _data = list(payload.to_bytes())
            self._log.debug("data type: {}; data: '{}'".format(type(_data), _data))
            self._i2cbus.write_block_data(self._i2c_address, self._config_register, _data)
            if verbose:
                self._log.info("payload written: " + Fore.WHITE + "'{}'".format(payload.to_string()))
            # read 1-byte response
            _read_data = self._i2cbus.read_byte_data(self._i2c_address, self._config_register)
            # convert response byte to Response
            _response = Response.from_value(_read_data)
            if _response is None:
                raise ValueError('null response.')
            elif not isinstance(_response, Response):
                raise ValueError('expected Response, not {}.'.format(type(_response)))
            elif _response != RESPONSE_OKAY:
                self._log.debug("response: {}".format(_response.description))
            else:
                self._log.error("error response: {}".format(_response.description))
            self._last_send_time = now # update only on success
            return _response
        except TimeoutError as te:
            self._log.error("transfer timeout: {}".format(te))
            return RESPONSE_CONNECTION_ERROR
        except Exception as e:
            self._log.error('{} raised writing payload: {}\n{}'.format(type(e), e, traceback.format_exc()))
            return RESPONSE_RUNTIME_ERROR

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def close(self):
        self._log.info("closing…")
        if self._i2cbus:
            self._i2cbus.close()
        self._log.info('closed.')

#EOF
