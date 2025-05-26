#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-05-06
# modified: 2025-05-24
#
# I2C/application response codes, provides an int value (e.g., 0x4F),
# a label (e.g., "REOK"), and a description (e.g., "okay").
#

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Response:
    _instances = []

    def __init__(self, value: int, label: str, description: str):
        self._value = value
        self._label = label
        self._description = description
        Response._instances.append(self)

    @property
    def value(self):
        return self._value

    @property
    def label(self):
        return self._label

    @property
    def description(self):
        return self._description

    @classmethod
    def from_value(cls, value: int):
        for instance in cls._instances:
            if instance.value == value:
                return instance
        return None

    @classmethod
    def from_label(cls, label: str):
        label = label.upper()
        for instance in cls._instances:
            if instance.label == label:
                return instance
        return None

    @classmethod
    def from_description(cls, description: str):
        description = description.lower()
        for instance in cls._instances:
            if instance.description == description:
                return instance
        return None

    @classmethod
    def from_label(cls, label):
        for instance in cls._instances:
            if instance.label == label:
                return instance
        return None

    def __int__(self):
        return self._value

    def __index__(self):
        return self._value  # Allows use in bytes(), bytearray(), etc.

    def __repr__(self):
        return f"<Response{self._label} (0x{self._value:02X})>"

    def __format__(self, format_spec):
        return format(self._value, format_spec)

    def __eq__(self, other):
        if isinstance(other, Response):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, str):
            # Compare case-insensitive against label or description
            return other.upper() == self.label or other.lower() == self.description.lower()
        return NotImplemented

# define response codes
RESPONSE_INIT               = Response(0x10, "REIN", "initial")
RESPONSE_STARTED            = Response(0x11, "REST", "started")
RESPONSE_COMPLETE           = Response(0x12, "RECO", "complete")
RESPONSE_OKAY               = Response(0x4F, "REOK", "okay")
RESPONSE_BAD_ADDRESS        = Response(0x71, "REBA", "bad address")
RESPONSE_BAD_REQUEST        = Response(0x72, "REBR", "bad request")
RESPONSE_OUT_OF_SYNC        = Response(0x73, "REOS", "out of sync")
RESPONSE_INVALID_CHAR       = Response(0x74, "REIC", "invalid character")
RESPONSE_SOURCE_TOO_LARGE   = Response(0x75, "RESL", "source too large")
RESPONSE_PAYLOAD_WRONG_SIZE = Response(0x76, "REPW", "payload wrong size")
RESPONSE_VALIDATED          = Response(0x77, "REUN", "validated")
RESPONSE_UNVALIDATED        = Response(0x78, "REUN", "unvalidated")
RESPONSE_EMPTY_PAYLOAD      = Response(0x79, "REEP", "empty payload")
RESPONSE_BUSY               = Response(0x80, "REBY", "busy")
RESPONSE_SKIPPED            = Response(0x81, "RESK", "skipped")
RESPONSE_CONNECTION_ERROR   = Response(0x82, "RECE", "connection error")
RESPONSE_RUNTIME_ERROR      = Response(0x83, "RERE", "runtime error")
RESPONSE_UNKNOWN_ERROR      = Response(0x84, "REUE", "unknown error")

#EOF
