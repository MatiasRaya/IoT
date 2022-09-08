import pycom
import time
import ubinascii
import ujson
import urequests
import airq
import connections

from sensors import Sensors
from network import Bluetooth
from machine import Timer
from pycoproc_1 import Pycoproc

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
VoC = 0
rssi = 0

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
# conections.lte_connection()
pycom.rgbled(YELLOW)
time.sleep(2)
pycom.rgbled(NO_COLOUR)

# Pytrack object and sensors
py = Pycoproc(Pycoproc.PYTRACK)
pySensor = Sensors(py)

data_sensor = {
    'variable' : '{}'.format(mac),
    'temperature': temperature,
    'pressure': pressure,
    'humidity': humidity,
    'gas_resistance': gas_resistance,
    'VoC': VoC,
    'rssi': rssi,
    'posLat' : pySensor.get_position().coordinates()[0],
    'posLon' : pySensor.get_position().coordinates()[0]
}

rate = {
    'transmission_rate' : 5,
    'sensor' : 1
}

chrono = Timer.Chrono()

def transmission_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
    print(data_sensor)
    sed_data()

def sensor_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(sensor_handler, rate['sensor'], periodic=True)
    position = pySensor.get_position().coordinates()
    data_bt()
    data_sensor['variable'] = '{}'.format(mac)
    data_sensor['temperature'] = temperature
    data_sensor['pressure'] = pressure
    data_sensor['humidity'] = humidity
    data_sensor['gas_resistance'] = gas_resistance
    data_sensor['VoC'] = VoC
    data_sensor['posLat'] = position[0]
    data_sensor['posLon'] = position[1]
    

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

def data_bt():
    global rssi, mac, gas_resistance, pressure, temperature, humidity, VoC
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
                        VoC = airq.air_quality_score(minor_f, gas_resistance)
                        break
        else:
            time.sleep(0.050)

def sed_data():
    try:
        response = post_data(SERVER_ADDRESS, stored_data())
    except Exception as e:
        print(e)
        print("POST attempet failed.")
        pycom.rgbled(RED)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)