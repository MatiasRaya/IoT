from L76GNSS import L76GNSS

class Sensors:
    sensors = {}
    def __init__(self,pytrack):
        self.sensors["position"]=L76GNSS(pytrack)

    def get_position(self):
        return self.sensors["position"]

    def __del__(self):
        print("Object deleted")