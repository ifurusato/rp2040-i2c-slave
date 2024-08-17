# RP2040 I2C Slave

![ItsyBitsy RP2040 on the MR01](./img/ItsyBitsyRP2040.jpg)

This provides a simple implementation for using an RP2040-based MCU as an 
I2C slave with a Raspberry Pi I2C master. It is easily modified to work 
with any RP2040 but has been developed and targeted for the Adafruit 
ItsyBitsy RP2040 with its NeoPixel as a status indicator.

This repository is largely based on the original work by TraoreMorike found at:

* [Raspberry-Pico---I2C-Slave](https://github.com/TraoreMorike/Raspberry-Pico---I2C-Slave)


## Hardware Installation

The ItsyBitsy RP2040 uses pin 24 for SDA and pin 25 for SCL. You should also
be sure to connect the GND pin to the common ground of your Raspberry Pi. If
you're connecting it to your Pi via a USB connector you won't need to provide
3.3V to the board as that will be provided via USB. So: just three wires, as
per the photo.


## Support & Liability

This project comes with no promise of support or liability. Use at your own risk.


## Copyright & License

This software is Copyright 2024 by Murray Altheim, All Rights Reserved.

Distributed under the MIT License, see LICENSE file included with project.

