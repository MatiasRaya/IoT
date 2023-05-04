import pycom
import time
import ubinascii
import ujson
import urequests
import math
import airq
import connections

from sensors import Sensors
from machine import Timer
from pycoproc_1 import Pycoproc
from network import Bluetooth

# Bluetooth connecton
bt = Bluetooth()
bt.init(antenna=bt.EXT_ANT)
bt.start_scan(-1)

# Global variable
mac = 0
rssi = 0
temperature = 0
humidity = 0
pressure = 0
gas_resistance = 0
voc = 0
rssi = 0
actualization1 = 2
actualization2 = 1

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
headers={'Content-Type':'application/json','Authorization':'90421b3f-9708-4738-ac31-f8052e4ef5b4','User-Agent':'LCD'}
# headers={'Content-Type':'application/json','Authorization':'531bc5a5-4e7b-433d-9f32-e605ac4e8a15','User-Agent':'LCD'}

# connections.wifi_connection()
connections.lte_connection()
pycom.rgbled(YELLOW)
time.sleep(2)
pycom.rgbled(NO_COLOUR)

# Pytrack object and sensors
py = Pycoproc(Pycoproc.PYTRACK)
pySensor = Sensors(py)

data_sensor = [
    {
        "variable" : "temperature{}".format(mac),
        "value" : temperature
    },
    {
        "variable" : "pressure{}".format(mac),
        "value" : pressure
    },
    {
        "variable" : "humidity{}".format(mac),
        "value" : humidity
    },
    {
        "variable" : "gas_resistance{}".format(mac),
        "value" : gas_resistance
    },
    {
        "variable" : "voc{}".format(mac),
        "value" : voc
    },
    {
        "variable" : "rssi{}".format(mac),
        "value" : rssi
    },
    {
        "variable" : "location{}".format(mac),
        "value" : rssi,
        "location" : {
            "lat" : pySensor.get_position().coordinates()[0],
            "lng" : pySensor.get_position().coordinates()[1]
        }
    },
]

rate = {
    'transmission_rate' : actualization1,
    'sensor' : actualization2
}

chrono = Timer.Chrono()

def transmission_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
    print("Por enviar")
    send_data()
    print("Enviado")

def sensor_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(sensor_handler, rate['sensor'], periodic=True)
    data_bt()
    data_sensor[0]["variable"] = 'temperature{}'.format(mac)
    data_sensor[0]["value"] = temperature
    data_sensor[1]["variable"] = 'pressure{}'.format(mac)
    data_sensor[1]["value"] = pressure
    data_sensor[2]["variable"] = 'humidity{}'.format(mac)
    data_sensor[2]["value"] = humidity
    data_sensor[3]["variable"] = 'gas_resistance{}'.format(mac)
    data_sensor[3]["value"] = gas_resistance
    data_sensor[4]["variable"] = 'voc{}'.format(mac)
    data_sensor[4]["value"] = voc
    data_sensor[5]["variable"] = 'rssi{}'.format(mac)
    data_sensor[5]["value"] = rssi
    data_sensor[6]["variable"] = 'location{}'.format(mac)
    data_sensor[6]["value"] = rssi
    data_sensor[6]["location"]["lat"] = pySensor.get_position().coordinates()[0]
    data_sensor[6]["location"]["lng"] = pySensor.get_position().coordinates()[1]
    rate["transmission_rate"] = actualization1
    rate["sensor"] = actualization2
    

chrono.start()

transmission_alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
sensor_rate = Timer.Alarm(sensor_handler, rate['sensor'], periodic=True)

alarm_sets = []

alarm_sets.append([transmission_alarm, transmission_handler, 'transmission_rate'])
alarm_sets.append([sensor_rate, sensor_handler, 'sensor'])

def data_bt():
    global rssi, mac, gas_resistance, pressure, temperature, humidity, voc
    while True:
        adv = bt.get_adv()
        if adv:
            read_adv = bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
            if read_adv == None:
                pass
            else:
                manuf_data = ubinascii.hexlify(read_adv[0:4])
                if(manuf_data == b'4c000215'):
                    rssi = adv.rssi
                    mac = int.from_bytes(adv.mac, "little")
                    uuid_raw = read_adv[4:20]
                    name, gas_resistance, pressure  = airq.byte_to_info(uuid=uuid_raw)
                    if name == "PyN":
                        major = ubinascii.hexlify(read_adv[20:22])
                        minor = ubinascii.hexlify(read_adv[22:24])
                        major_int = int(major, 16)
                        major_f = major_int/100
                        minor_int = int(minor,16)
                        minor_f = minor_int/100
                        temperature = major_f
                        humidity = minor_f
                        voc = airq.air_quality_score(minor_f, gas_resistance)
                        break
        else:
            time.sleep(0.050)

def stored_data():
    store_data = {}
    store_data = data_sensor
    json_store_data = ujson.dumps(store_data)
    return json_store_data

def post_data(address, raw_data):
    response = urequests.post(address, headers=headers, data=raw_data)
    return response

def get_data(address):
    response = urequests.get(address, headers=headers)
    aux = response.json()
    return aux

def send_data():
    global actualization1, actualization2
    try:
        print(data_sensor)
        if (data_sensor[6]["location"]["lat"] is not None) and (rssi > -70) and (mac != 0):
            print("Se envio")
            response = post_data(SERVER_ADDRESS, stored_data())
            pycom.rgbled(CIAN)
            time.sleep(1)
            pycom.rgbled(NO_COLOUR)
    except Exception as e:
        print(e)
        print("POST attempet failed.")
        pycom.rgbled(RED)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)

    # try:
    #     response = get_data(SERVER_ADDRESS)
    #     aux1 = list(filter(lambda actual: actual["variable"] == "actualization1", list(filter(lambda actual: actual["variable"] == "actualization1", response["result"]))))[0]["value"]
    #     aux2 = list(filter(lambda actual: actual["variable"] == "actualization2", list(filter(lambda actual: actual["variable"] == "actualization2", response["result"]))))[0]["value"]
    #     if aux1 >= 5:
    #         actualization1 = aux1
    #     if aux2 >= 1:
    #         actualization2 = aux2
    # except Exception as e:
    #     print(e)
    #     print("GET attempet failed.")
    #     pycom.rgbled(BLUE)
    #     time.sleep(1)
    #     pycom.rgbled(NO_COLOUR)