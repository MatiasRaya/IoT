import pycom
import machine
import urequests
import time
import ujson

from network import WLAN
from sensors import Sensors
from pycoproc_1 import Pycoproc
from machine import Timer, RTC
from urequests import Response

# Global variable
iteration = 0

# Colors indicator led
RED = 0x7f0000
GREEN = 0x007f00
BLUE = 0x00007f
YELLOW = 0x7f7f00
WHITE = 0x7f7f7f
PINK = 0x7f007f
CIAN = 0x007f7f
ORANGE = 0xd35400
NO_COLOUR = 0x000000

pycom.heartbeat(False)

pycom.rgbled(ORANGE)
time.sleep(5)
pycom.rgbled(NO_COLOUR)

# WiFi connectation
SERVER_ADDRESS = "http://192.168.1.142" # LCD
# SERVER_ADDRESS = "" # APP HEROKU
SERVER_PORT = "5000"

wlan = WLAN(mode=WLAN.STA)
wlan.connect('LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
print('Network found!')
while not wlan.isconnected():
    machine.idle()
print('WLAN connection succeeded!')
pycom.rgbled(YELLOW)
time.sleep(2)
pycom.rgbled(NO_COLOUR)

# Pysense object and sensors
py = Pycoproc(Pycoproc.PYSENSE)
pySensor = Sensors(py)

data_sensor = {
    'nodo' : 1,
    'iteration' : iteration,
    'lightB' : pySensor.get_lightB(),
    'lightR' : pySensor.get_lightR(),
    'humidity' : pySensor.get_humidity(),
    'temperature' : pySensor.get_temperature(),
    'altitude' : pySensor.get_altitude()
}

rate = {
    'transmission_rate': 2,
    'light_rate': 1,
    'humidity_rate': 1,
    'temperature_rate': 1,
    'altitude_rate': 1
}

# Chrono definition and inicialization
chrono = Timer.Chrono()

# def transmission_handler(alarm):
#     alarm.cancel()
#     alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)

def light_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(light_handler, rate['light_rate'], periodic=True)
    data_sensor['lightB'] = pySensor.get_lightB()
    data_sensor['lightR'] = pySensor.get_lightR()

def humidity_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(humidity_handler, rate['humidity_rate'], periodic=True)
    data_sensor['humidity'] = pySensor.get_humidity()

def temperature_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(temperature_handler, rate['temperature_rate'], periodic=True)
    data_sensor['temperature'] = pySensor.get_temperature()

def altitude_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(altitude_handler, rate['altitude_rate'], periodic=True)
    data_sensor['altitude'] = pySensor.get_altitude()

chrono.start()

# transmission_alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
light_rate = Timer.Alarm(light_handler, rate['light_rate'], periodic=True)
humidity_rate = Timer.Alarm(humidity_handler, rate['humidity_rate'], periodic=True)
temperature_rate = Timer.Alarm(temperature_handler, rate['temperature_rate'], periodic=True)
altitude_rate = Timer.Alarm(altitude_handler, rate['altitude_rate'], periodic=True)

alarm_sets = []

# alarm_sets.append([transmission_alarm, transmission_handler, 'transmission_rate'])
alarm_sets.append([light_rate, light_handler, 'light_rate'])
alarm_sets.append([humidity_rate, humidity_handler, 'humidity_rate'])
alarm_sets.append([temperature_rate, temperature_handler, 'temperature_rate'])
alarm_sets.append([altitude_rate, altitude_handler, 'altitude_rate'])

def stored_data(interval):
    store_data = {}
    time.sleep(interval)
    data_sensor['iteration'] = iteration
    store_data = data_sensor
    json_store_data = ujson.dumps(store_data)
    return json_store_data

def post_method(address, raw_data):
    response = urequests.post(address, data=raw_data)
    return response

def get_method(address):
    response = urequests.get(address)
    return response

def delete_table():
    try:
        response = get_method(SERVER_ADDRESS + ":" + SERVER_PORT + "/delete/" + data_sensor['nodo'])
        pycom.rgbled(CIAN)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
    except Exception as e:
        print(e)

delete_table()

for i in range(12):
    store_data = stored_data(5)
    try:
        response = post_method(SERVER_ADDRESS + ":" + SERVER_PORT + "/data", store_data)
        pycom.rgbled(GREEN)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
        iteration += 1
    except Exception as e:
        print(e)
        response = ''
        print("POST attempet failed.")
        pycom.rgbled(RED)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)

    print(iteration)