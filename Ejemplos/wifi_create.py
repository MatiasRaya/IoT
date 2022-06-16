from network import WLAN
import machine
wlan = WLAN()

#wlan.init(mode=WLAN.AP, ssid='hello world')
#use the line below to apply a password
wlan.init(mode=WLAN.AP, ssid="hi", auth=(WLAN.WPA2, "12345678"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface



wlan = WLAN(mode=WLAN.STA_AP)

nets = wlan.scan()
for net in nets:

    if net.ssid == 'LCD3':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '1cdunc0rd0ba'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        pycom.rgbled(0x7f0000)
        break