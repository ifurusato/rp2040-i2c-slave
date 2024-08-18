# RP2040 I2C Slave

![ItsyBitsy RP2040 on the MR01](./img/ItsyBitsyRP2040.jpg)

This provides a simple implementation for using an RP2040-based MCU as an
I2C slave with a Raspberry Pi I2C master, sending a one-way message of up
to 32 ASCII characters to the slave from the master, returning a single
byte as status. There is currently no facility for returning longer messages,
though anyone wishing to contribute code to provide that feature is most
welcome to do so.

It is easily modified to work with any RP2040 but has been developed and
targeted for the Adafruit ItsyBitsy RP2040 with its NeoPixel as a status
indicator.

The implementation uses Python (CPython) on the Raspberry Pi and MicroPython
on the RP2040. It communicates over I2C address `0x44`, though this is easily
changed.

The I2C communications of this repository are largely based on (and include
two files from) the original work by TraoreMorike as found at:

* [Raspberry-Pico---I2C-Slave](https://github.com/TraoreMorike/Raspberry-Pico---I2C-Slave)


## Dependencies

There are no external dependencies apart from a recent version of MicroPython,
which can be downloaded from:

* [MicroPython downloads](https://micropython.org/download/)

This project is currently using MicroPython v1.23.0.

A handy tool for working with MicroPython is rshell, available at:

* [rshell](https://github.com/dhylands/rshell)


## Installation/Deployment

Once you've installed a recent version of MicroPython on your RP2040 board,
the easiest way to deploy the code and test the project is using *rshell*.

For discussion purposes, let's assume you've cloned the repository to the
following directory: `/home/pi/workspace/rp2040-i2c-slave/`, with its
MicroPython files in the `/upy/` subdirectory.

If your RP2040 board is showing up at `/dev/ttyACM1` you'd start an rshell
session with:
```
  % rshell -p /dev/ttyACM1
  /home/pi/workspace/rp2040-i2c-slave/upy>
```
then change the working directory to the board itself:
```
  % cd /pyboard
  /pyboard>
```
Then you can copy the files to the board in one go using the `rsync` command,
where the `.` indicates the current working directory:
```
  /pyboard> rsync /home/pi/workspace/rp2040-i2c-slave/upy .
  Adding /pyboard/neopixel.py
  Adding /pyboard/RP2040_I2C_Registers.py
  Adding /pyboard/stringbuilder.py
  [...]
```
Then you can either `exit` rshell and push the board's RST button to execute
the main.py script, or enter the Python REPL and `import main` (you don't
include the file extension) to execute its code:
```
  /pyboard> repl
  MicroPython v1.23.0 on 2024-06-02; Adafruit ItsyBitsy RP2040 with RP2040
  Type "help()" for more information.
  >>>
  >>> import main
```
This will start I2C slave mode on the RP2040. If you're using an ItsyBitsy
RP2040 you should see its NeoPixel flash a bright cyan blue three times,
and then a dimmer continuous flash after that.


## Testing

You can then test to see if things are working by executing the `master.py`
file with a string argument:
```
 % master.py "This is something important."
  -- value "This is something important."
  creating connection to I2C bus on address 0x44…
  writing I2C payload of 28 chars: 'This is something important.'…
  writing completion code…
  write complete.
```
Note that this only supports ASCII strings of up to 32 characters between
SPACE and `~`. The response will be something like:
```
  read data: '32'
  response: okay
  complete.
```


## Next Steps

The next phase of this project will be to convert both the `master.py` on the
Pi and the `main.py` on the slave to Python classes, so they can be more easily
extended and used as base classes.


## Usage

Copy the contents of the `./upy/` directory on an RP2040 that has a recent
version of MicroPython installed. The "main.py" file is used for the ItsyBitsy
RP2040 and includes use of its NeoPixel. If you're using a different RP2040
board you can use the "main_no_px.py" file instead, as that has no NeoPixel
support and therefore should be pretty generic. If you want to use the latter
you'd need to rename it to "main.py".

On the Raspberry Pi side, the provided "master.py" file expects a command
line argument, which must be composed of a maximum of 32 ASCII characters
between SPACE (32) and "~" (126). For example,
```
  % master.py "Send this message."
```

The I2C slave will receive the message and respond with a single byte status
indicator. The hardcoded values can be found in the MicroPython slave file:
```
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
```
On the Raspbery Pi side there is an Enum matching these values.


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

