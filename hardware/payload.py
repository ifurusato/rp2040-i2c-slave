#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-05-01
# modified: 2025-05-26

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Payload:
    PACKET_LENGTH = 32  # 31-byte payload + 1-byte CRC
    '''
    The Payload class is designed to convey a fixed length payload over I2C.

    Each packet is exactly 32 bytes (256 bits):

      * Command (32 chars): WS-padded ASCII string identifying the command 
      * CRC (1 byte): A CRC-8-CCITT checksum for error detection
    '''
    def __init__(self, command):
        if len(command) > (self.PACKET_LENGTH - 1):
            raise ValueError("Command must be less than {} characters.".format(self.PACKET_LENGTH - 1))
        self._command = command

    @property
    def command(self):
        '''
        Return the command string.
        '''
        return self._command

    @staticmethod
    def _crc8_ccitt(data):
        '''
        Compute CRC-8-CCITT checksum over the given byte sequence.
        Polynomial: x^8 + x^2 + x + 1 (0x07)
        '''
        crc = 0
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x07) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc

    def to_bytes(self):
        '''
        Encode command as 32 character payload to bytes: 31 ASCII characters + 1 CRC byte = 32 bytes.
        '''
        payload = (self._command + ' ' * 31)[:31].encode('ascii') # pad or truncate, then encode in one line
        crc = self._crc8_ccitt(payload)
        return payload + bytes([crc])

    @classmethod
    def from_bytes(cls, packet_bytes):
        '''
        Decode a 32-byte packet (31 bytes ASCII + 1 CRC) into a Payload instance,
        validating the CRC.
        '''
        if len(packet_bytes) != cls.PACKET_LENGTH:
            raise ValueError("Expected {}-byte packet".format(cls.PACKET_LENGTH))
        payload = packet_bytes[:31]
        received_crc = packet_bytes[31]
        expected_crc = cls._crc8_ccitt(payload)
        if received_crc != expected_crc:
            raise ValueError(f"CRC mismatch: got {received_crc:02X}, expected {expected_crc:02X}")
        try:
            payload_str = payload.decode()
        except UnicodeDecodeError:
            raise ValueError("Payload is not valid ASCII.")
        command = payload_str.strip()
        return cls(command)

    def to_string(self) -> str:
        '''
        Return a human-readable string representation of the payload.
        '''
        return "command: '{}'".format(self._command)

    def __repr__(self):
        '''
        Return a concise string representation for debugging.
        '''
        return "Payload(command='{}')".format(self._command)

    def __eq__(self, other):
        '''
        Check if another Payload instance is equal to this one.
        '''
        if not isinstance(other, Payload):
            return NotImplemented
        return (self._command == other._command)

#EOF
