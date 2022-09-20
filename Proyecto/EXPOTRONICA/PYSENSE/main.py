import pycom
import time
import ujson
import urequests
import machine
import ubinascii
import connections

from sensors import Sensors
from machine import Timer
from pycoproc_1 import Pycoproc

# Global variable
mac = int.from_bytes(ubinascii.hexlify(machine.unique_id()), "little")
temperature = 0
pressure = 0
humidity = 0
lightB = 0
lightR = 0
accelerationX = 0
accelerationY = 0
accelerationZ = 0
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
headers={'Content-Type':'application/json','Authorization':'d17cd84f-d5b0-4e45-b139-4b85fefec6a6','User-Agent':'LCD'}
# headers={'Content-Type':'application/json','Authorization':'531bc5a5-4e7b-433d-9f32-e605ac4e8a15','User-Agent':'LCD'}

connections.wifi_connection()
# connections.lte_connection()
pycom.rgbled(YELLOW)
time.sleep(2)
pycom.rgbled(NO_COLOUR)

# Pytrack object and sensors
py = Pycoproc(Pycoproc.PYSENSE)
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
        "variable" : "lightB{}".format(mac),
        "value" : lightB
    },
    {
        "variable" : "lightR{}".format(mac),
        "value" : lightR
    },
    {
        "variable" : "accelerationX{}".format(mac),
        "value" : accelerationX
    },
    {
        "variable" : "accelerationY{}".format(mac),
        "value" : accelerationY
    },
    {
        "variable" : "accelerationZ{}".format(mac),
        "value" : accelerationZ
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
    data_sensor[0]["variable"] = 'temperature{}'.format(mac)
    data_sensor[0]["value"] = temperature
    data_sensor[1]["variable"] = 'pressure{}'.format(mac)
    data_sensor[1]["value"] = pressure
    data_sensor[2]["variable"] = 'humidity{}'.format(mac)
    data_sensor[2]["value"] = humidity
    data_sensor[3]["variable"] = 'lightB{}'.format(mac)
    data_sensor[3]["value"] = pySensor.get_light()[0]
    data_sensor[4]["variable"] = 'lightR{}'.format(mac)
    data_sensor[4]["value"] = pySensor.get_light()[0]
    data_sensor[5]["variable"] = 'accelerationX{}'.format(mac)
    data_sensor[5]["value"] = pySensor.get_acceleration()[0]
    data_sensor[6]["variable"] = 'accelerationY{}'.format(mac)
    data_sensor[6]["value"] = pySensor.get_acceleration()[1]
    data_sensor[7]["variable"] = 'accelerationZ{}'.format(mac)
    data_sensor[7]["value"] = pySensor.get_acceleration()[2]
    rate["transmission_rate"] = actualization1
    rate["sensor"] = actualization2
    

chrono.start()

transmission_alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
sensor_rate = Timer.Alarm(sensor_handler, rate['sensor'], periodic=True)

alarm_sets = []

alarm_sets.append([transmission_alarm, transmission_handler, 'transmission_rate'])
alarm_sets.append([sensor_rate, sensor_handler, 'sensor'])

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
        print("Se envio")
        # response = post_data(SERVER_ADDRESS, stored_data())
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