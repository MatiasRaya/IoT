from network import WLAN
import machine
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