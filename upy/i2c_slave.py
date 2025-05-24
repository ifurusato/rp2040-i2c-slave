#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-14
# modified: 2025-05-03
#
# Wraps an I2C Slave to pass payloads to a Controller class.

import sys
import utime
from machine import Pin
from rp2040_slave import RP2040_Slave

from core.logger import Level, Logger
from colors import*
from colorama import Fore, Style
from payload import Payload
from response import*

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class I2CSlave:
    ERROR_LIMIT = 10  # max errors before exiting main loop
    '''
    Wraps an RP2040_Slave to provide a processing loop and a connection
    to a Controller to handle I2C transactions.
    '''
    def __init__(self, i2c_bus_id=None, sda=None, scl=None, i2c_address=None, display=None, controller=None, level=Level.INFO):
        super().__init__()
        self._log = Logger('i2c_slave', level)
        self._log.debug("I2C slave starting…")
        self._display    = None
        self._controller = controller
        self.s_i2c       = RP2040_Slave(i2c_id=i2c_bus_id, sda=sda, scl=scl, i2c_address=i2c_address)
        self.state       = self.s_i2c.I2CStateMachine.I2C_START
        _data_buffer     = []
        _address         = 0x00
        self._currentTransaction = self.s_i2c.I2CTransaction(_address, _data_buffer)
        self._errors     = 0
        self._enabled = False
        self._log.info('ready.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

    def enable(self):
        self._log.info("enabling controller…")
        self._enabled = True
        self._controller.enable()
        self._i2c_loop()

    def disable(self):
        self._log.info("disabling controller…")
        self._enabled = False
        self._controller.disable()
        self._log.info("disabled.")

    def show_color(self, color):
        '''
        Show the color on the color display.
        '''
        if self._display:
            self._display.show_color(color)

    def _i2c_loop(self):
        self._log.info("starting main loop…")
        while self._enabled and self._controller.enabled:
            response = RESPONSE_INIT
            try:
                if self._errors > self.ERROR_LIMIT:
                    self._log.error("reached error limit.")
                    self.show_color(COLOR_RED)
                    self.disable()
                    return      
                self.state = self.s_i2c.handle_event()
                if self.state == self.s_i2c.I2CStateMachine.I2C_START:
                    self._log.info("💮 I2C_START")
                    response = RESPONSE_STARTED
                if self.state == self.s_i2c.I2CStateMachine.I2C_RECEIVE:
                    response = self._handle_receive()
                if self.state == self.s_i2c.I2CStateMachine.I2C_REQUEST:
                    self._handle_request(response)
                    response = RESPONSE_COMPLETE
                if self.state == self.s_i2c.I2CStateMachine.I2C_FINISH:
                    response = self._handle_finish()
                    self.reset_transaction()
            except Exception as e:
                self._log.error("{} raised in I2C transaction: {}".format(type(e), e))
                sys.print_exception(e)
                self.reset_transaction()
                self._errors += 1
            utime.sleep(0.01) # minimal delay to prevent a tight loop
        self._log.info("I2C main loop stopped.")

    def _handle_receive(self):
        rx_step = 0
        rx_count = 0
        expected_length = 0

        while self.s_i2c.Available():
            byte = self.s_i2c.Read_Data_Received()

            if rx_step == 0:
                if byte == 0x01: # start marker
                    rx_step = 1
                    rx_count = 0
                else:
                    self._log.debug(f"Ignoring unexpected byte: {byte}")

            elif rx_step == 1:
                expected_length = byte
                rx_step = 2
                self._currentTransaction.reset()

            elif rx_step == 2:
                self._currentTransaction.append_data_byte(byte)
                rx_count += 1
                if rx_count >= expected_length:
                    rx_step = 3

            elif rx_step == 3:
                if self._controller: # halt timer if it's running
                    self._controller.stop()
                if byte == 0x01:  # end marker
                    self._log.info("received end marker.")
                    return RESPONSE_VALIDATED
                else:
                    self._log.error(f"Invalid end marker: {byte}")
                    return RESPONSE_UNVALIDATED
        return RESPONSE_BAD_REQUEST

    def _handle_request(self, response):
        self._log.info("sending response: '{}'".format(response.description))
        while self.s_i2c.is_Master_Req_Read():
            self.s_i2c.Slave_Write_Data(response.value)

    def _handle_finish(self):
        if self._currentTransaction.data_length() == Payload.PACKET_LENGTH:
            payload = Payload.from_bytes(self._currentTransaction.data_as_bytes())
            response = self._controller.process_payload(payload)
            self._log.info("received response: '{}'".format(response.description))
            return response
        else:
            self._log.error("expected {}, not {} bytes in payload.".format(
                    Payload.PACKET_LENGTH, self._currentTransaction.data_length()))
            return RESPONSE_PAYLOAD_WRONG_SIZE

    def reset_transaction(self):
        self._currentTransaction.reset()

#EOF
