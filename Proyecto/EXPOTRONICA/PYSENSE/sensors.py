from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,PRESSURE
from LIS2HH12 import LIS2HH12

class Sensors:
    sensors = {}
    def __init__(self, pysense):
        self.sensors["light"] = LTR329ALS01(pysense)
        self.sensors["humidity"] = SI7006A20(pysense)
        self.sensors["temperature"] = SI7006A20(pysense)
        self.sensors["pressure"] = MPL3115A2(pysense, mode=PRESSURE)
        self.sensors["acceleration"] = LIS2HH12(pysense)
    
    def get_light(self):
        return self.sensors["light"].light()
    
    def get_humidity(self):
        return self.sensors["humidity"].humidity()
    
    def get_pressure(self):
        return self.sensors["pressure"].pressure()

    def get_temperature(self):
        return self.sensors["temperature"].temperature()

    def get_acceleration(self):
        return self.sensors["acceleration"].acceleration()
    
    def __del__(self):
        print("Object deleted")