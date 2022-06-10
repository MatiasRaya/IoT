from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='RAYA 2.4', auth=(WLAN.WPA2, 'Rayaplasencia1996'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())