#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-05-24
# modified: 2025-05-24

class AbstractDisplay:
    def show_color(self, color):
        raise NotImplementedError("must implement show_color(color)")

#EOF
