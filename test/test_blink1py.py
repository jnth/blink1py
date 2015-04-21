#!/usr/bin/en python
# coding: utf-8

""" Test this library : you must have a Blink(1) device. """


import unittest
from blink1py.blink1 import Blink1


class TestBlink1(unittest.TestCase):
    def setUp(self):
        self.b = Blink1()

    def test_init(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
