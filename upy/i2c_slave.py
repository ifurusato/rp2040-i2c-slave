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
    RESPONSE_32 = True
    BATCH_WRITE = True
    '''
    Wraps an RP2040_Slave to provide a processing loop and a connection
    to a Controller to handle I2C transactions.
    '''
    def __init__(self, name=None, i2c_bus_id=None, sda=None, scl=None, i2c_address=None, display=None, controller=None, level=Level.INFO):
        super().__init__()
        self._log = Logger('i2c_s:{}'.format(name), level)
        self._log.debug("I2C slave starting…")
        self._display    = display
        self._controller = controller
        self.s_i2c       = RP2040_Slave(i2c_id=i2c_bus_id, sda=sda, scl=scl, i2c_address=i2c_address)
        self.state       = self.s_i2c.I2CStateMachine.I2C_START
        _data_buffer     = []
        _address         = 0x00
        self._currentTransaction = self.s_i2c.I2CTransaction(_address, _data_buffer)
        self._errors     = 0
        self._enabled    = False
        self._log.info('ready.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

    def enable(self):
        self._log.info("enabling controller…")
        self._enabled = True
        self._controller.enable()
        self._i2c_loop()

    def disable(self):
        self._log.debug("disabling controller…")
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
        response = RESPONSE_INIT
        while self._enabled and self._controller.enabled:
            try:
                if self._errors > self.ERROR_LIMIT:
                    self._log.error("reached error limit.")
                    self.show_color(COLOR_RED)
                    self.disable()
                    return
                self.state = self.s_i2c.handle_event()
                if self.state == self.s_i2c.I2CStateMachine.I2C_START:
                    response = self._handle_start()
                if self.state == self.s_i2c.I2CStateMachine.I2C_RECEIVE:
                    start_time = utime.ticks_ms()
                    response = self._handle_receive()
                if self.state == self.s_i2c.I2CStateMachine.I2C_REQUEST:
                    response = self._handle_request(response)
                    # report how fast the request was handled
                    _elapsed_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
                    self._log.info("request returned: {}ms elapsed.".format(_elapsed_ms))
                if self.state == self.s_i2c.I2CStateMachine.I2C_FINISH:
                    response = self._handle_finish()
                    # report how fast the complete process took
                    _elapsed_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
                    self._log.info(Style.DIM + "request complete: {}ms elapsed.".format(_elapsed_ms))
                    self.reset_transaction()
            except Exception as e:
                self._log.error("{} raised in I2C transaction: {}".format(type(e), e))
                sys.print_exception(e)
                self.reset_transaction()
                self._errors += 1
            utime.sleep(0.01) # minimal delay to prevent a tight loop
        self._log.info("main loop stopped.")

    def _handle_start(self):
        return RESPONSE_STARTED

    def _handle_receive(self):
        rx_step         = 0
        rx_count        = 0
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
                if byte == 0x01:  # end marker
#                   self._log.debug("received end marker.")
                    if self._controller:
                        self._controller.validated()
#                   return RESPONSE_OKAY
                    return RESPONSE_VALIDATED
                else:
                    self._log.error(f"Invalid end marker: {byte}")
                    return RESPONSE_UNVALIDATED
        return RESPONSE_BAD_REQUEST

    def _handle_request(self, response):
        if self.RESPONSE_32:
#           self._log.debug("writing MULTIBYTE response: '{}'…".format(response.description))
            if response == RESPONSE_VALIDATED:
                # if validated return OKAY
                response = RESPONSE_OKAY
            # create a Payload from the response description
            response_payload = Payload(response.description)
            # convert the Payload to bytes, which includes data and CRC
            response_bytes = response_payload.to_bytes()
            if self.BATCH_WRITE:
                # This writes 8 bytes in a batch as soon as the FIFO has space, waiting only when
                # the FIFO is full, not after every byte. More efficient than single byte writes.
                fifo_size = 8
                idx = 0
                length = len(response_bytes)
                while idx < length:
                    # wait until FIFO not full to write at least one byte
                    while not self.s_i2c.is_Master_Req_Read():
                        utime.sleep_us(100)
                    # write up to fifo_size bytes or remaining bytes
                    bytes_to_write = min(fifo_size, length - idx)
                    for i in range(bytes_to_write):
                        self.s_i2c.Slave_Write_Data(response_bytes[idx + i])
                    idx += bytes_to_write
            else:
                # send the response bytes over I2C
                for byte in response_bytes:
                    while not self.s_i2c.is_Master_Req_Read():
                        utime.sleep_us(100)
                    self.s_i2c.Slave_Write_Data(byte)
        else:
#           self._log.debug("writing 1 byte response: '{}' of 0x{:02X}…".format(response.description, response.value))
            while self.s_i2c.is_Master_Req_Read():
                self.s_i2c.Slave_Write_Data(response.value)
#           self._log.debug("response written.")
        return RESPONSE_COMPLETE

    def _handle_finish(self):
        if self._currentTransaction.data_length() == Payload.PACKET_LENGTH:
            payload = Payload.from_bytes(self._currentTransaction.data_as_bytes())
            response = self._controller.process_payload(payload)
#           self._log.debug("received response: '{}'".format(response.description))
            return response
        else:
            self._log.error("expected {}, not {} bytes in payload.".format(
                    Payload.PACKET_LENGTH, self._currentTransaction.data_length()))
            return RESPONSE_PAYLOAD_WRONG_SIZE

    def reset_transaction(self):
        self._currentTransaction.reset()
        self._errors = 0

#EOF
