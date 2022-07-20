from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

class Sensors:
    sensors = {}
    def __init__(self, pysense):
        self.sensors["lightB"]=LTR329ALS01(pysense)
        self.sensors["lightR"]=LTR329ALS01(pysense)
        self.sensors["humidity"]=SI7006A20(pysense)
        self.sensors["temperature"]=SI7006A20(pysense)
        self.sensors["pressure"]=MPL3115A2(pysense, mode=PRESSURE)
    
    def get_lightB(self):
        return self.sensors["lightB"].lightB()

    def get_lightR(self):
        return self.sensors["lightR"].lightR()
    
    def get_humidity(self):
        return self.sensors["humidity"].humidity()
    
    def get_temperature(self):
        return self.sensors["temperature"].temperature()

    def get_pressure(self):
        return self.sensors["pressure"].pressure()
    
    def __del__(self):
        print("Object deleted")