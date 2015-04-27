#!/usr/bin/en python
# coding: utf-8

""" Testing Class.
You must have one device plug into your computer.
"""


import unittest
from blink1py import Blink1, hex2rgb


class TestFunctions(unittest.TestCase):
    def test_hex2rgb(self):
        self.assertEqual(hex2rgb('#ff0000'), (255, 0, 0))
        self.assertEqual(hex2rgb('ff0000'), (255, 0, 0))
        self.assertEqual(hex2rgb('#000000'), (0, 0, 0))
        self.assertEqual(hex2rgb('#123456'), (18, 52, 86))
        self.assertEqual(hex2rgb('#abcdef'), (171, 205, 239))


class TestBlink1Properties(unittest.TestCase):
    def setUp(self):
        self.b = Blink1()

    def tearDown(self):
        self.b.close()

    def test_vid(self):
        self.assertEqual(self.b.vid, '0x27b8')

    def test_pid(self):
        self.assertEqual(self.b.pid, '0x01ed')

    def test_serialnum(self):
        self.assertEqual(len(self.b.serialnum), 8)


class TestBlink1(unittest.TestCase):
    def setUp(self):
        self.b = Blink1()

    def tearDown(self):
        self.b.close()

    def test_01_white_1s(self):
        self.b.on(duration=1)  # white during 1 second

    def test_02_purple_2s(self):
        self.b.set_rgb(*hex2rgb('#ff00f0'), duration=2)  # purple during 2 seconds

    def test_03_off(self):
        self.b.off(duration=0.5)  # pause

    def test_04_fade_color(self):
        self.b.fade_rgb(*hex2rgb('#FA5882'), t=0.5, duration=1)

    def test_05_pause(self):
        self.b.pause(0.5)  # alias to b.off()

    def test_06_two_leds(self):
        self.b.set_rgbn(led1=(255, 0, 0), led2=(0, 255, 0), duration=1)
        self.b.pause(0.5)

    def test_07_two_leds_with_swapping(self):
        self.b.set_rgbn(led1=(255, 0, 0), led2=(0, 0, 255), duration=0.5, swap=10)  # police car !
        self.b.pause(1)

    def test_08_rainbow(self):
        self.b.rainbow()
        self.b.pause(1)

    def test_09_random(self):
        self.b.random(n=10, duration=0.3)
        self.b.pause(1)


if __name__ == '__main__':
    unittest.main()
