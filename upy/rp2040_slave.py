#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-04-26
# modified: 2025-05-24
# origin:   i2cSlave.py by Morike Traore
#
# I2C Slave Mode Intructions:
#            https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
#

from machine import mem32
from RP2040_I2C_Registers import*

from core.logger import Level, Logger

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class RP2040_Slave:

    IO_BANK0_BASE = 0x40014000

    # Atomic Register Access
    MEM_RW  = 0x0000  # Normal read/write access
    MEM_XOR = 0x1000  # XOR on write
    MEM_SET = 0x2000  # Bitmask set on write
    MEM_CLR = 0x3000  # Bitmask clear on write

    '''
    No defaults.

    :param i2c_id:         the I2C bus ID (0 or 1)
    :param sda:            the SDA pin
    :param sdc:            the SCL pin
    :param i2c_address:    the I2C address
    '''
    def __init__(self, i2c_id=None, sda=None, scl=None, i2c_address=None):
        self._log = Logger('rp2040_slave', Level.INFO)
        self._scl = scl
        self._sda = sda
        self._i2c_address = i2c_address
        if i2c_id is None:
            raise ValueError('no value for i2c_id provided.')
        elif i2c_id == 0:
            self._i2c_base = 0x40044000 # I2C0_BASE 
        else:
            self._i2c_base = 0x40048000 # I2C1_BASE 

        # 1. Disable the DW_apb_i2c by writing a ‘0’ to IC_ENABLE.ENABLE
        self.RP2040_Clear_32b_i2c_Reg(I2C_OFFSET["I2C_IC_ENABLE"],
                                  self.get_Bits_Mask("ENABLE", I2C_IC_ENABLE))

        # 2. Write to the IC_SAR register (bits 9:0) to set the slave address.
        # This is the address to which the DW_apb_i2c responds.
        self.RP2040_Clear_32b_i2c_Reg(I2C_OFFSET["I2C_IC_SAR"],
                                  self.get_Bits_Mask("IC_SAR", I2C_IC_SAR))

        self.RP2040_Set_32b_i2c_Reg(I2C_OFFSET["I2C_IC_SAR"],
                                self._i2c_address & self.get_Bits_Mask("IC_SAR", I2C_IC_SAR))

        # 3. Write to the IC_CON register to specify which type of addressing 
        # is supported (7-bit or 10-bit by setting bit 3).
        # Enable the DW_apb_i2c in slave-only mode by writing a ‘0’ into bit 
        # six (IC_SLAVE_DISABLE) and a ‘0’ to bit zero (MASTER_MODE).

        # Disable Master mode
        self.RP2040_Clear_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CON"],
                                      self.get_Bits_Mask("MASTER_MODE", I2C_IC_CON))
        # Enable slave mode
        self.RP2040_Clear_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CON"],
                                      self.get_Bits_Mask("IC_SLAVE_DISABLE", I2C_IC_CON))
        # Enable clock strech
        self.RP2040_Set_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CON"],
                                      self.get_Bits_Mask("RX_FIFO_FULL_HLD_CTRL", I2C_IC_CON))

        # 4. Enable the DW_apb_i2c by writing a ‘1’ to IC_ENABLE.ENABLE.
        self.RP2040_Set_32b_i2c_Reg(I2C_OFFSET["I2C_IC_ENABLE"],
                                self.get_Bits_Mask("IC_ENABLE", I2C_IC_ENABLE))

        # Reset GPIO0 function
        mem32[ self.IO_BANK0_BASE | self.MEM_CLR | ( 4 + 8 * self._sda) ] = 0x1f
        # Set GPIO0 as IC0_SDA function
        mem32[ self.IO_BANK0_BASE | self.MEM_SET | ( 4 + 8 * self._sda) ] = 0x03

        # Reset GPIO1 function
        mem32[ self.IO_BANK0_BASE | self.MEM_CLR | ( 4 + 8 * self._scl) ] = 0x1f
        # Set GPIO1 as IC0_SCL function
        mem32[ self.IO_BANK0_BASE | self.MEM_SET | ( 4 + 8 * self._scl) ] = 3

        self._log.info('established I2C slave on ID={}; SDA={}; SCL={} at 0x{:02X}'.format(i2c_id, sda, scl, self._i2c_address))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    class I2CStateMachine:
        I2C_RECEIVE = 0
        I2C_REQUEST = 1
        I2C_FINISH  = 2
        I2C_START   = 3

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    class I2CTransaction:

        def __init__(self, address: int, data_byte: list):
            self._address   = address
            self._data_byte = data_byte
            
        # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        @property
        def address(self):
            return self._address
    
        # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        def reset(self):
            self._address = 0x00
            self._data_byte = []

        # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        def append_data_byte(self, byte: int):
            if not (0 <= byte <= 255):
                raise ValueError("byte must be in range 0–255")
            self._data_byte.append(byte)

        # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        def data_length(self) -> int:
            return len(self._data_byte)

        # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        def data_as_bytes(self) -> bytes:
            return bytes(self._data_byte)

        # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
        def data_as_string(self) -> str:
            return bytes(self._data_byte[:11]).decode('ascii')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def get_Bits_Mask(self, bits, register):
        """ This function return the bit mask based on bit name """
        bits_to_clear = bits
        bit_mask = sum([key for key, value in register.items() if value in bits_to_clear])
        return bit_mask

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def RP2040_Write_32b_i2c_Reg(self, register, data, atr=0):
        """ Write RP2040 I2C 32bits register """
        # < Base Addr > | < Atomic Register Access > | < Register >
        mem32[self._i2c_base | atr | register] = data

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def RP2040_Set_32b_i2c_Reg(self, register, data):
        """ Set bits in RP2040 I2C 32bits register """
        # < Base Addr > | 0x2000 | < Register >
        self.RP2040_Write_32b_i2c_Reg(register, data, atr=self.MEM_SET)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def RP2040_Clear_32b_i2c_Reg(self, register, data):
        """ Clear bits in RP2040 I2C 32bits register """
        # < Base Addr > | 0x3000 | < Register >
        self.RP2040_Write_32b_i2c_Reg(register, data, atr=self.MEM_CLR)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def RP2040_Read_32b_i2c_Reg(self, offset):
        """ Read RP2040 I2C 32bits register """
        return mem32[self._i2c_base | offset]

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def RP2040_Get_32b_i2c_Bits(self, offset, bit_mask):
        return mem32[self._i2c_base | offset] & bit_mask

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def handle_event(self):

        # I2C Master has abort the transactions
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_INTR_STAT"],
                                 self.get_Bits_Mask("R_TX_ABRT", I2C_IC_INTR_STAT))):
            # Clear int
            self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_TX_ABRT"])
            return RP2040_Slave.I2CStateMachine.I2C_FINISH

        # Last byte transmitted by I2C Slave but NACK from I2C Master
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_INTR_STAT"],
                                 self.get_Bits_Mask("R_RX_DONE", I2C_IC_INTR_STAT))):
            # Clear int
            self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_RX_DONE"])
            return RP2040_Slave.I2CStateMachine.I2C_FINISH

        # Restart condition detected
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_INTR_STAT"],
                                 self.get_Bits_Mask("R_RESTART_DET", I2C_IC_INTR_STAT))):
            # Clear int
            self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_RESTART_DET"])


        # Start condition detected by I2C Slave
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_INTR_STAT"],
                                 self.get_Bits_Mask("R_START_DET", I2C_IC_INTR_STAT))):
            # Clear start detection
            self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_START_DET"])
            return RP2040_Slave.I2CStateMachine.I2C_START

        # Stop condition detected by I2C Slave
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_INTR_STAT"],
                                 self.get_Bits_Mask("R_STOP_DET", I2C_IC_INTR_STAT))):

            # Clear stop detection
            self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_STOP_DET"])
            return RP2040_Slave.I2CStateMachine.I2C_FINISH

        # Check if RX FIFO is not empty
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_STATUS"],
                                 self.get_Bits_Mask("RFNE", I2C_IC_STATUS))):

            return RP2040_Slave.I2CStateMachine.I2C_RECEIVE

        # Check if Master is requesting data
        if (self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_INTR_STAT"],
                                 self.get_Bits_Mask("R_RD_REQ", I2C_IC_INTR_STAT))):

            # Shall Wait until transfer is done, timing recommended 10 * fastest SCL clock period
            # for 100 Khz = (1/100E3) * 10 = 100 uS
            # for 400 Khz = (1/400E3) * 10 = 25 uS

            return RP2040_Slave.I2CStateMachine.I2C_REQUEST

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def is_Master_Req_Read(self):
        """ Return status if I2C Master is requesting a read sequence """

        # Check RD_REQ Interrupt bit (master wants to read data from the slave)
        status = self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_RAW_INTR_STAT"],
                                 self.get_Bits_Mask("RD_REQ", I2C_IC_RAW_INTR_STAT))

        if status :
            return True
        return False

    '''
    def is_Master_Req_Seq_Write(self):
        # Return true if I2C Master is requesting a sequential data writing

        # Check whether is FIRST_DATA_BYTE bit is active in IC_DATA_CMD.
        first_data_byte_stat = self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_DATA_CMD"],
                                 self.get_Bits_Mask("FIRST_DATA_BYTE", I2C_IC_DATA_CMD))

        # Check whether is STOP_DET_IFADDRESSED bit is active in IC_CON.
        stop_stat = self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_CON"],
                                 self.get_Bits_Mask("STOP_DET_IFADDRESSED", I2C_IC_CON))

        if (stop_stat):
            # Clear stop bit int
            self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_STOP_DET"])

        # Master sequential write true if FIRST_DATA_BYTE bit is active and no stop condition detected.
        if first_data_byte_stat and not(stop_stat):
            return True
        return False
    '''

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def Slave_Write_Data(self, data):
        '''
        Write 8bits of data at destination of I2C Master.
        '''
        # Send data
        self.RP2040_Write_32b_i2c_Reg(I2C_OFFSET["I2C_IC_DATA_CMD"], data &
                                  self.get_Bits_Mask("DAT", I2C_IC_DATA_CMD))

        self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_CLR_RD_REQ"])

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def Available(self):
        '''
        Return true if data has been received from I2C Master.
        '''
        # Get RFNE Bit (Receive FIFO Not Empty)
        return self.RP2040_Get_32b_i2c_Bits(I2C_OFFSET["I2C_IC_STATUS"],
                                self.get_Bits_Mask("RFNE", I2C_IC_STATUS))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def Read_Data_Received(self):
        '''
        Return data from I2C Master.
        '''
        return self.RP2040_Read_32b_i2c_Reg(I2C_OFFSET["I2C_IC_DATA_CMD"]) &  self.get_Bits_Mask("DAT", I2C_IC_DATA_CMD)

#   if __name__ == "__main__":
#       #import utime
#       import machine
#       from machine import mem32
#       from rp2040_slave import RP2040_Slave
#
#       # Initialize an empty buffer list for sequential write sequences
#
#       data_buf = []
#       addr = 0x00
#
#       s_i2c = RP2040_Slave(0,sda=0,scl=1,i2c_address=0x44)
#       state = s_i2c.I2CStateMachine.I2C_START
#       currentTransaction = s_i2c.I2CTransaction(addr, data_buf)
#
#       counter = 0
#
#
#       print("I2C Slave test")
#       try:
#           while True:
#
#               state = s_i2c.handle_event()
#
#               if state == s_i2c.I2CStateMachine.I2C_START:
#                   pass
#
#               if state == s_i2c.I2CStateMachine.I2C_RECEIVE:
#                   if currentTransaction.address == 0x00:
#                       # First byte received is the register address
#                       currentTransaction.address = s_i2c.Read_Data_Received()
#
#                   # Read all data byte received until RX FIFO is empty
#                   while (s_i2c.Available()):
#                       currentTransaction.data_byte.append(s_i2c.Read_Data_Received())
#                       # Virtually Increase register address
#                       # s_i2c.I2CTransaction.address += 1
#
#               if state == s_i2c.I2CStateMachine.I2C_REQUEST:
#                   # Send some dummy data back
#                   while (s_i2c.is_Master_Req_Read()):
#                       counter += 1
#                       s_i2c.Slave_Write_Data(counter)
#
#                       # Virtually Increase register address
#                       # s_i2c.I2CTransaction.address += 1
#                       print ("Sendind data : ", counter)
#
#               if state == s_i2c.I2CStateMachine.I2C_FINISH:
#                   print ("Register : ", currentTransaction.address ,"Received : ", currentTransaction.data_byte)
#
#                   currentTransaction.address = 0x00
#                   currentTransaction.data_byte = []
#
#       except KeyboardInterrupt:
#           pass

#EOF
