from time import time
import time
import pycom

delay = 1

red = 0x7f0000
green = 0x007f00
blue = 0x00007f
yellow = 0x7f7f00
white = 0x7f7f7f

pycom.heartbeat(False)

for cycles in range(10):
    pycom.rgbled(red)
    time.sleep(delay)

    pycom.rgbled(green)
    time.sleep(delay)

    pycom.rgbled(blue)
    time.sleep(delay)

    pycom.rgbled(yellow)
    time.sleep(delay)

    pycom.rgbled(white)
    time.sleep(delay)