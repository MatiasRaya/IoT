import pycom
import time
import ubinascii
import ujson
import urequests
import connections

# Colors indicator led
RED = 0x7f0000
GREEN = 0x007f00
BLUE = 0x00007f
YELLOW = 0x7f7f00
WHITE = 0x7f7f7f
PINK = 0x7f007f
CIAN = 0x007f7f
NO_COLOUR = 0x000000

pycom.heartbeat(False)

pycom.rgbled(GREEN)
time.sleep(5)
pycom.rgbled(NO_COLOUR)

# wifi connection 
SERVER_ADDRESS = "https://api.tago.io/data"
headers={'Content-Type':'application/json','Authorization':'531bc5a5-4e7b-433d-9f32-e605ac4e8a15'}

connections.wifi_connection()
# connections.lte_connection()
pycom.rgbled(YELLOW)
time.sleep(2)
pycom.rgbled(NO_COLOUR)

def get_iteration(address):
    response = urequests.get(address,headers=headers)
    aux = response.json()
    return aux

def prueba():
    try:
        respuesta = get_iteration(SERVER_ADDRESS)
        print(respuesta["result"])
        p = list(filter(lambda actual: actual["variable"] == "actualization1", list(filter(lambda actual: actual["variable"] == "actualization1", respuesta["result"]))))[0]["value"]
        print(p)
    except Exception as e:
        print(e)


prueba()