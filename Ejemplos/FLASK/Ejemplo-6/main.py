import time
from network import WLAN
import machine
import pycom

from urequests import Response
import urequests
import ujson


# SERVER_ADDRESS = "http://192.168.1.142"
# SERVER_ADDRESS = "http://127.0.0.1"
SERVER_ADDRESS = "http://192.168.0.13" #Buscar la segun address porque con la primera hay problema
SERVER_PORT = "5000"

count = 0

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'RAYA 2.4':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'Rayaplasencia1996'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        pycom.rgbled(0x7a007c)
        break

    if net.ssid == 'LCD3':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '1cdunc0rd0ba'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        print(wlan.ifconfig())
        pycom.rgbled(0x7f0000)
        break

def post_method(address, raw_data):
    response = urequests.post(address, data=raw_data)
    return response

def stored_data():
    store_data = {
        "name" : "Matias",
        "age" : count,
        "university" : "UNC"
    }
    json_store_data = ujson.dumps(store_data)
    return json_store_data

while True:
    # time.sleep(1)
    try:
        response = post_method(SERVER_ADDRESS + ":" + SERVER_PORT + "/tasks/", stored_data())
        # print(response.content)
        response.close()
        pycom.rgbled(0x007f00)
        count += 1
        # time.sleep(2)
        pycom.rgbled(0x7f007f)
        # time.sleep(3)
    except Exception as e:
        print(e)
        response = ''
        print("POST attempet failed.")
        pycom.rgbled(0x00007f)
        time.sleep(2)
    # time.sleep(1)
    pycom.rgbled(0x4a007f)
    print(count)