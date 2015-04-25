#!/usr/bin/env python
# coding: utf-8

from __future__ import division
import blink1_raw as b1raw
import time
import random
import colorsys


def hex2rgb(color):
    """ Convert hex color value to (r, g, b) tuple.
    :param color: hex color value ('#xxxxxx' or 'xxxxxx' format)
    :return: (r, g, b)
    """
    if len(color) == 7:
        color = color[1:]
    parts = [color[e:e+2] for e in range(0, 6, 2)]
    return tuple([int(e, base=16) for e in parts])


class Blink1NotFoundError(Exception):
    pass


class Blink1Error(Exception):
    pass


class Blink1:
    def __init__(self, id=None, serial=None, path=None):
        self._open_blink1(id, serial, path)
        self.__closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def _open_blink1(self, id, serial, path):
        if id is not None:
            blink1 = b1raw.open_by_id(id)
        elif serial is not None:
            blink1 = b1raw.open_by_serial(serial)
        elif path is not None:
            blink1 = b1raw.open_by_path(path)
        else:
            blink1 = b1raw.blink1_open()
        if not blink1:
            raise Blink1NotFoundError(
                'blink(1) library could not find a blink(1) device')
        self._device = blink1

    def close(self):
        if not self.__closed:
            try:
                b1raw.blink1_close(self._device)
            finally:
                self.__closed = True

    def play(self, pos=0):
        b1raw.play(self._device, 1, pos)

    def stop(self, pos=0):
        b1raw.play(self._device, 0, pos)

    def set_pattern(self, pos, r=0, g=0, b=0, t=0):
        b1raw.write_pattern_line(self._device, t, r, g, b, pos)

    def read_pattern(self, pos):
        t, r, g, b = b1raw.read_pattern_line(self._device, pos)
        return r, g, b, t

    def off(self, duration=None):
        """ Turn the leds off
        :param duration: pause in seconds or None to set unlimited time.
        """
        self.set_rgb(0, 0, 0)
        if duration is not None:
            time.sleep(duration)

    def pause(self, t):
        """ Pause.
        :param t: duration of the pause in seconds.
        """
        self.off(duration=t)

    def on(self, duration=None):
        """ Turn the leds on (white)
        :param duration: duration in seconds or None to set unlimited time.
        """
        self.set_rgb(255, 255, 255)
        if duration is not None:
            time.sleep(duration)
            self.off()

    def set_rgb(self, r=0, g=0, b=0, n=0, duration=None):
        """ Turn the led on a specific color.
        :param r: red color from 0 to 255.
        :param g: green color from 0 to 255.
        :param b: blue color from 0 to 255.
        :param n: led number (1:top, 2:bottom, 0:both).
        :param duration: duration in seconds or None to set unlimited time.
        :return:
        """
        b1raw.fade_to_rgb(self._device, 0, r, g, b, n)
        if duration is not None:
            time.sleep(duration)
            self.off()

    def fade_rgb(self, r=0, g=0, b=0, t=0, n=0, duration=None):
        """ Fade to RGB.
        :param r: red color from 0 to 255.
        :param g: green color from 0 to 255.
        :param b: blue color from 0 to 255.
        :param t: fadding time in seconds.
        :param n: led number (1:top, 2:bottom, 0:both).
        :param duration: duration in seconds or None to set unlimited time.
        """
        tms = int(t * 1000)  # convert into ms.
        b1raw.fade_to_rgb(self._device, tms, r, g, b, n)
        if duration is not None:
            time.sleep(duration + t)
            self.fade_rgb(t=t)
            time.sleep(t)  # wait for the led to fade off.

    def set_rgbn(self, led1, led2, duration=None, swap=None):
        """ Turn the leds on two specific colors.
        :param led1: tuple of (r, g, b)
        :param led2: tuple of (r, g, b)
        :param duration: duration in seconds or None to set unlimited time.
        :param swap: swap the two leds for 'swap' times.
        """
        if swap is None:
            swap = 1
        r1, g1, b1 = led1
        r2, g2, b2 = led2
        l1, l2 = 1, 2
        for i in xrange(swap):
            b1raw.fade_to_rgb(self._device, 0, r1, g1, b1, l1)
            b1raw.fade_to_rgb(self._device, 0, r2, g2, b2, l2)
            if duration is not None:
                time.sleep(duration)
            l1, l2 = l2, l1  # swap
        if duration is not None:
            self.off()

    def random(self, n=5, duration=1):
        """ Random color (hue part of hsv colorspace).
        :param n: number of random colors.
        :param duration: duration in seconds for each color.
        """
        for i in xrange(n):
            h = random.random()  # random hue
            r, g, b = [int(e) for e in colorsys.hsv_to_rgb(h, 1, 255)]
            self.set_rgb(r, g, b, duration=duration)

    def rainbow(self, duration=0.1):
        """ Rainbow color pattern.
        :param duration: duration in seconds for each color.
        """
        for h in [e / 100. for e in xrange(0, 101, 2)]:
            r, g, b = [int(e) for e in colorsys.hsv_to_rgb(h, 1, 255)]
            self.fade_rgb(r, g, b, t=duration)
            time.sleep(duration)
        self.off()