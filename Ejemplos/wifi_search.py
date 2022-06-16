from network import WLAN
import machine
import pycom

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    print(net.ssid)