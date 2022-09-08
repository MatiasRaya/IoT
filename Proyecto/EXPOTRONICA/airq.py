import connections
import time
import ubinascii
import struct
import math

def byte_to_info(uuid):
    gas_res_d = 0
    name = uuid[0:3]
    name_text = ''.join(chr(t) for t in name)
    if name_text == "PyN":
        sensor_id = uuid[7]
        mac = ubinascii.hexlify(uuid[10:16])
        press = ubinascii.hexlify(uuid[8:10])
        press_d = int(press, 16)
        gas_res = ubinascii.hexlify(uuid[3:7])
        gas_res_d = int(gas_res, 16)
        # print("{} {} BLE_MAC: {}, Pressure: {} hPa, Gas resistance: {} ohm".format(name_text, sensor_id, mac, press_d, gas_res_d), end=", ")
    return (name_text,gas_res_d, press_d)

def air_quality_score(hum, gas_res):
    gas_reference = 250000
    hum_reference = 40
    gas_lower_limit = 5000
    gas_upper_limit = 50000
    # Verificamos el puntaje de la humedad
    if (hum >= 38 and hum <= 42):
        hum_score = 0.25*100
    else:
        if (hum < 38):
            hum_score = 0.25/hum_reference*hum*100
        else:
            hum_score = ((-0.25/(100-hum_reference)*hum)+0.416666)*100
    # Obtenemos la referencia del gas
    if (gas_reference > gas_upper_limit):
        gas_reference = gas_upper_limit
    if (gas_reference < gas_lower_limit):
        gas_reference = gas_lower_limit
    # Calculamos el puntaje del gas
    gas_score = (0.75/(gas_upper_limit-gas_lower_limit)*gas_reference -(gas_lower_limit*(0.75/(gas_upper_limit-gas_lower_limit))))*100
    # Calculamos la calidad del aire en interiores
    air_quality_score = hum_score + gas_score

    # print("IAQ score:", air_quality_score)

    return(air_quality_score)

    # print("Air quality is", end=" ")
    # # Calculamos la calidad del aire y determinamos su calidad
    # air_quality_score = (100-air_quality_score)*5
    # if (air_quality_score >= 301):
    #     print("Hazardous")
    # elif (air_quality_score >= 201 and air_quality_score <= 300 ):
    #     print("Very Unhealthy")
    # elif (air_quality_score >= 176 and air_quality_score <= 200 ):
    #     print("Unhealthy")
    # elif (air_quality_score >= 151 and air_quality_score <= 175 ):
    #     print("Unhealthy for Sensitive Groups")
    # elif (air_quality_score >=  51 and air_quality_score <= 150 ):
    #     print("Moderate")
    # elif (air_quality_score >=  00 and air_quality_score <=  50 ):
    #     print("Good")