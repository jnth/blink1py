========
blink1py
========

Blink(1) python library (wrapper of the C library).


Prerequesites
=============

1. Make the blink1 library (see `blink1/commandline <https://github.com/todbot/blink1/tree/master/commandline>`_)

2. Rename the blink1 library to ``libblink1.so.0.0`` (or something that
will resolve as blink1) and add it to your path (ie ldconfig)


Usage
=====

Example ::

    from blink1py import Blink1
    import time

    b = Blink1()
    b.set_rgb(255, 0, 0)  # set to red
    b.on()  # set to white
    time.sleep(1)  # wait for 1 second
    b.off()  # turn the led off
    b.close()

In a more effective way ::

    b.on(duration=1)
    b.set_rgb(0, 0, 255, duration=2)  # set to blue for 2 seconds

Example using the `with` statement ::

    from blink1py import Blink1

    with Blink1() as b:
        b.on()
        b.set_rgb(255, 0, 255, duration=1)

Pause ::

    b.pause(0.5)  # pause of 0.5 second, alias of b.off()

Using hexadecimal color values ::

    from blink1py import Blink1, hex2rgb

    with Blink1() as b:
        b.set_rgb(*hex2rgb('#ff0000'), duration=2)

Two different colors at the leds ::

    b.set_rgbn(led1=(255, 0, 0), led2=(0, 0, 255), duration=2)

Create pattern ::

    b.set_rgbn(led1=(255, 0, 0), led2=(0, 0, 255), duration=0.5, swap=10)  # police car !

Fadding colors ::

    b.fade_rgb(255, 0, 125, t=1)  # 1 second fadding color
    b.fade_rgb(255, 0, 0, t=0.5, n=2)  # ... with red at the 2nd led
    b.fade_rgb(0, 0, 255, t=0.2, duration=3)  # ... blue for 3 seconds

Random colors ::

    b.random()  # five random colors
    b.random(n=10, duration=0.2)  # ten random colors of 0.2 seconds

Rainbow colors ::

    b.rainbow()
