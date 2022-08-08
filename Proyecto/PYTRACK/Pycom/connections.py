import machine
import time

from network import WLAN, LTE

def wifi_connection():
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect('LCD', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
    print('Network found!')
    while not wlan.isconnected():
        machine.idle()
    print('WLAN connection succeeded!')

def lte_connection():
    lte = LTE()
    lte.attach(band=28, apn="datos.personal.com")
    # lte.attach(band=28, apn="igprs.claro.com.ar")
    while not lte.isattached():
        time.sleep(0.25)
        print('.',end='')
    lte.connect()
    while not lte.isconnected():
        time.sleep(0.25)
    print('LTE connection succeeded!')