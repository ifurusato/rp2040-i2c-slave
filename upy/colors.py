#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2024-08-14
# modified: 2025-05-25
#
# color constants ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

class Color:
    def __init__(self, r, g, b, description):
        self._rgb = (r, g, b)
        self._description = description

    def __iter__(self):
        return iter(self._rgb) # enables unpacking

    def __getitem__(self, index):
        return self._rgb[index] # enables tuple-style access

    def __len__(self):
        return len(self._rgb)

    def __repr__(self):
        return f"Color{self._rgb} - {self._description}"

    @property
    def description(self):
        return self._description

# define colors
COLOR_BLACK        = Color(  0,   0,   0, "black")
COLOR_RED          = Color(255,   0,   0, "red")
COLOR_GREEN        = Color(  0, 255,   0, "green")
COLOR_BLUE         = Color(  0,   0, 255, "blue")
COLOR_CYAN         = Color(  0, 255, 255, "cyan")
COLOR_MAGENTA      = Color(255,   0, 255, "magenta")
COLOR_YELLOW       = Color(250, 150,   0, "yellow")

COLOR_SKY_BLUE     = Color(  8,  64,  96, "sky blue")
COLOR_YELLOW_GREEN = Color( 96, 255,   0, "yellow-green")
COLOR_DARK_RED     = Color( 32,   0,   0, "dark red")
COLOR_DARK_GREEN   = Color(  0,  32,   0, "dark green")
COLOR_DARK_BLUE    = Color(  0,   0,  32, "dark blue")
COLOR_DARK_CYAN    = Color(  0,  32,  32, "dark cyan")
COLOR_DARK_GREY    = Color( 12,  12,  12, "dark grey")
COLOR_ORANGE       = Color(220,  96,   0, "orange")
COLOR_INDIGO       = Color(  0,  75, 130, "indigo")
COLOR_VIOLET       = Color(138,  43, 226, "violet")
COLOR_DARK_VIOLET  = Color( 42,  12,  64, "dark violet")

#                       R    G    B
# COLOR_BLACK        = (  0,   0,   0)
# COLOR_RED          = (255,   0,   0)
# COLOR_GREEN        = (  0, 255,   0)
# COLOR_BLUE         = (  0,   0, 255)
# COLOR_CYAN         = (  0, 255, 255)
# COLOR_MAGENTA      = (255,   0, 255)
# COLOR_YELLOW       = (250, 150,   0)
# 
# COLOR_SKY_BLUE     = (  8,  64,  96)
# COLOR_YELLOW_GREEN = ( 96, 255,   0)
# COLOR_DARK_RED     = ( 32,   0,   0)
# COLOR_DARK_GREEN   = (  0,  32,   0)
# COLOR_DARK_BLUE    = (  0,   0,  32)
# COLOR_DARK_CYAN    = (  0,  32,  32)
# COLOR_DARK_GREY    = ( 12,  12,  12)
# COLOR_ORANGE       = (220,  96,   0)
# COLOR_INDIGO       = (  0,  75, 130)
# COLOR_VIOLET       = ( 138, 43, 226)
# COLOR_DARK_VIOLET  = ( 42,  12,  64)

#EOF
