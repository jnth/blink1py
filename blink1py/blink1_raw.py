#!/usr/bin/env python
# coding: utf-8

""" Blink(1) raw control with ctypes
"""

import os
import sys
from ctypes import CDLL, c_int, c_char_p, c_wchar_p, c_void_p, c_ushort, c_ubyte, byref
from ctypes.util import find_library


class Blink1LibraryError(Exception):
    pass


# Find the C library
if 'win' in sys.platform:  # Windows OS: use the dll here
    whereami = os.path.dirname(os.path.realpath(__file__))
    libblink1 = CDLL(os.path.join(whereami, "blink1-lib"))

else:  # Other OS: try to find it
    libname = find_library("blink1")
    if not libname:
        raise Blink1LibraryError('blink(1) library not found')
    libblink1 = CDLL(libname)


blink1_open = libblink1.blink1_open
blink1_open.restype = c_void_p


blink1_close = libblink1.blink1_close
blink1_close.argtypes = [c_void_p]


openByPath = libblink1.blink1_openByPath
openByPath.restype = c_void_p
openByPath.argtypes = [c_char_p]


def open_by_path(path):
    return openByPath(path)


openBySerial = libblink1.blink1_openBySerial
openBySerial.restype = c_void_p
openBySerial.argtypes = [c_wchar_p]


def open_by_serial(serial):
    return openBySerial(serial)


openById = libblink1.blink1_openById
openById.restype = c_void_p
openById.argtypes = [c_int]


def open_by_id(id):
    return openById(id)


fadeToRGB = libblink1.blink1_fadeToRGBN
fadeToRGB.argtypes = [c_void_p, c_ushort, c_ubyte, c_ubyte, c_ubyte]


def fade_to_rgb(device, time, r, g, b, n):
    time = c_ushort(time)
    r = c_ubyte(r)
    g = c_ubyte(g)
    b = c_ubyte(b)
    n = c_ubyte(n)
    return fadeToRGB(device, time, r, g, b, n)


_play = libblink1.blink1_play
_play.argtypes = [c_void_p, c_ubyte, c_ubyte]


def play(device, play, pos):
    play = c_ubyte(play)
    pos = c_ubyte(pos)
    _play(device, play, pos)


writePatternLine = libblink1.blink1_writePatternLine
writePatternLine.argtypes = [c_void_p, c_ushort, c_ubyte, c_ubyte, c_ubyte, c_ubyte]


def write_pattern_line(device, time, r, g, b, pos):
    time = c_ushort(time)
    r = c_ubyte(r)
    g = c_ubyte(g)
    b = c_ubyte(b)
    pos = c_ubyte(pos)
    writePatternLine(device, time, r, g, b, pos)


readPatternLine = libblink1.blink1_readPatternLine
readPatternLine.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_ubyte]


def read_pattern_line(device, pos):
    time = c_ushort()
    r = c_ubyte()
    g = c_ubyte()
    b = c_ubyte()
    pos = c_ubyte(pos)
    readPatternLine(device, byref(time), byref(r), byref(g), byref(b), pos)
    return int(time.value), int(r.value), int(g.value), int(b.value)