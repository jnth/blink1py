#!/usr/bin/env python
# coding: utf-8

""" Testing Blink(1) control class.
"""


from blink1py import Blink1, hex2rgb

with Blink1() as b:
    print(b)

    b.on(duration=1)  # white during 1 second
    b.set_rgb(*hex2rgb('#ff00f0'), duration=2)  # purple during 2 seconds
    b.off(duration=0.5)  # pause
    b.fade_rgb(*hex2rgb('#FA5882'), t=0.5, duration=1)
    b.pause(0.5)  # alias to b.off()
    b.set_rgbn(led1=(255, 0, 0), led2=(0, 255, 0), duration=1)
    b.pause(0.5)
    b.set_rgbn(led1=(255, 0, 0), led2=(0, 0, 255), duration=0.5, swap=10)  # police car !
    b.pause(1)
    b.rainbow()
    b.pause(1)
    b.random(n=10, duration=0.3)

