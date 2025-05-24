# A very cheap version of Colorama for MicroPython
#
# Copyright 2025 by Murray Altheim. All rights reserved. This file is part of
# the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-04-20
# modified: 2024-04-20
#
# Usage:
#
#    from colorama import Fore, Style
#
#    print(Fore.RED + "That's all, folks!" + Style.RESET)
#

class Fore:

    BLACK      = "\033[30m"
    RED        = "\033[31m"
    GREEN      = "\033[32m"
    YELLOW     = "\033[33m"
    BLUE       = "\033[34m"
    MAGENTA    = "\033[35m"
    CYAN       = "\033[36m"
    WHITE      = "\033[37m"
    RESET      = "\033[39m"
    LT_GREY    = "\033[37m"
    DK_GREY    = "\033[90m"
    LT_RED     = "\033[91m"
    LT_GREEN   = "\033[92m"
    LT_YELLOW  = "\033[93m"
    LT_BLUE    = "\033[94m"
    LT_MAGENTA = "\033[95m"
    LT_CYAN    = "\033[96m"

    def __init__(self):
        super().__init__()
        pass

class Style:

    RESET_ALL  = "\033[0m"
    NORMAL     = "\033[22m"
    BRIGHT     = "\033[1m"
    DIM        = "\033[2m"
    ITALIC     = "\033[3m"
    UNDERLINE  = "\033[4m"
    BLINKING   = "\033[5m"

    def __init__(self):
        super().__init__()
        pass

