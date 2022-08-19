from network import WLAN
import machine
import pycom

wlan = WLAN(mode=WLAN.STA)

wlan.antenna(WLAN.EXT_ANT)

nets = wlan.scan()
for net in nets:
    print(net.ssid)