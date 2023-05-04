from network import WLAN
import machine
import pycom

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'RAYA 2.4':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'Rayaplasencia1996'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

    if net.ssid == 'LCD3':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '1cdunc0rd0ba'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        pycom.rgbled(0x7f0000)
        break