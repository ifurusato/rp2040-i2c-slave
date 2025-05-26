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

import argparse
import sys, traceback
import time
from datetime import datetime as dt
from colorama import init, Fore, Style
init()

from core.logger import Logger, Level
from core.controller import Controller
from core.payload import Payload
from core.response import*

def parse_args():
    # create the argument parser
    parser = argparse.ArgumentParser(description="Process command and optional speeds/duration.")
    # command (required) and optional arguments with defaults
    parser.add_argument("command", type=str, help="The command to execute.")
    return parser.parse_args()

def main():

    _log = Logger('main', Level.INFO)
    _controller = None

    try:

        _log.info('controller begin…')

        _controller = Controller(i2c_bus=1, i2c_address=0x43)

        # parse the arguments
        _args = parse_args()

        start_time = dt.now()
        _response = _controller.send_payload(_args.command)
        elapsed_ms = (dt.now() - start_time).total_seconds() * 1000.0
        if _response is None:
            raise ValueError('null response.')
        elif isinstance(_response, Response):
            if _response != RESPONSE_OKAY:
                _log.info("response: {}; {:5.2f}ms elapsed.".format(_response.description, elapsed_ms))
            else:
                _log.warning("response: {}; {:5.2f}ms elapsed.".format(_response.description, elapsed_ms))
        elif not isinstance(_response, Response):
            raise ValueError('expected Response, not {}.'.format(type(_response)))
        else:
            _log.error("error response: {}; {:5.2f}ms elapsed.".format(_response.description, elapsed_ms))

    except KeyboardInterrupt:
        print("Program interrupted by user (Ctrl+C). Exiting gracefully.")
    except ValueError as e:
        # handle any CLI validation errors
        _log.error("parsing command line: {}".format(e))
    except TimeoutError as te:
        _log.error('transfer timeout: {}'.format(te))
    except Exception as e:
        _log.error('{} encountered: {}\n{}'.format(type(e), e, traceback.format_exc()))
    finally:
        _log.info('complete.')
        if _controller:
            _controller.close()

if __name__ == "__main__":
    main()

#EOF
