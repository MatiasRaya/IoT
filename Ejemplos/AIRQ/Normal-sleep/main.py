from network import Bluetooth
import time
import ubinascii
import struct
import math

# Declaramos una variable que hace referencia a la funcion de conexion Bluetooth
bt = Bluetooth()
bt.init(antenna=Bluetooth.EXT_ANT)
# Se inicia el escaneo sin tiempo de espera
bt.start_scan(-1)

def twoscmp(value):
    if value > 128:
        value = value - 256
    return value

def byte_to_info(uuid):
    gas_res_d = 0
    # Del arreglo de byte que recibimos, las primeras 3 posiciones son el nombre del dispositivo
    name = uuid[0:3]
    # Convertimos los bytes en texto
    name_text = ''.join(chr(t) for t in name)
    # Si el texto que obtuvimos es PyN, accedemos
    if name_text == "PyN":
        # La septima posicion del uuid corresponde al id del sensor
        sensor_id = uuid[7]
        # Obtenemos la direccio mac del dispositivo
        mac = ubinascii.hexlify(uuid[10:16])
        # Obtenemos la presion, que viene en el uuid desde la posicion 8 a la 9
        press = ubinascii.hexlify(uuid[8:10])
        # Convertimos el valor hexadecimal de la presion a decimal
        press_d = int(press, 16)
        # Obtenemos la resistencia del gas, que viene en el uuid desde la posicion 3 a la 6
        gas_res = ubinascii.hexlify(uuid[3:7])
        # Convertimos el valor hexadecimal de la resistencia del gas a decimal, es la cantidad de VOC (Volatile Organic Compounds, Compuestos Organicos Volatiles)
        gas_res_d = int(gas_res, 16)
        print("{} {} BLE_MAC: {}, Pressure: {} hPa, Gas resistance: {} ohm".format(name_text, sensor_id, mac, press_d, gas_res_d), end=", ")
    # Retornamos el nombre del dispositivo y la resistencia del gas
    return (name_text,gas_res_d)

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

    print("IAQ score:", air_quality_score)

    print("Air quality is", end=" ")
    # Calculamos la calidad del aire y determinamos su calidad
    air_quality_score = (100-air_quality_score)*5
    if (air_quality_score >= 301):
        print("Hazardous")
    elif (air_quality_score >= 201 and air_quality_score <= 300 ):
        print("Very Unhealthy")
    elif (air_quality_score >= 176 and air_quality_score <= 200 ):
        print("Unhealthy")
    elif (air_quality_score >= 151 and air_quality_score <= 175 ):
        print("Unhealthy for Sensitive Groups")
    elif (air_quality_score >=  51 and air_quality_score <= 150 ):
        print("Moderate")
    elif (air_quality_score >=  00 and air_quality_score <=  50 ):
        print("Good")

while True:
    # Obtenemos la tupla con el nombre del dispositivo que se conecto
    adv = bt.get_adv()
    if adv:
        # Buscamos un determinado dato dentro de lo que recibimos, si no está, nos devuelve None
        read_adv = bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
        # Verificamos si se obtuvo el dato que se esperaba, en este caso, el fabricante
        if read_adv==None:
            pass
        else:
            # Convertimos los datos binarios de lo que obtuvimos de la placa en un hexadecimal
            manuf = ubinascii.hexlify(read_adv)
            # Obtenemos los primeros 4 elementos del arreglo que obtuvimos anterormente
            manuf_data = ubinascii.hexlify(read_adv[0:4])
            # Verifiamos que el id coincide con el producto nuestro
            if (manuf_data == b'4c000215') :#or (manuf_data == b'd2000215')):# company id=d2 is Dialog, b'4c000215' is Apple's id and it implies ibeacon
                print(adv.rssi)
                print(adv.mac)
                # Obtenemos la direccion mac de nestro aparato
                print("mac:", ubinascii.hexlify(adv.mac))
                # Obtenemos el UUID de nuestro dispositivo
                uuid_raw = read_adv[4:20]
                uuid = ubinascii.hexlify(uuid_raw)
                # Llamamos a la funcion byte_to_info para convertir los bytes del uuid en informacion
                name, air=byte_to_info(uuid_raw)
                # Verificamos que el nombre del dispositivo sea el que estamos esperando
                if name == "PyN":
                    # Imprimimos la fuerza de la señal que recibimos
                    print("rssi:",adv.rssi)
                    # Obtenemos el numero mayor de la transmision del dispositivo
                    major = ubinascii.hexlify(read_adv[20:22])
                    # Obtenemos el numero menor de la transmision del dispositivo
                    minor = ubinascii.hexlify(read_adv[22:24])
                    # Obtenemos la potencia de transmision del dispositivo
                    tx_power = ubinascii.hexlify(read_adv[24:25])
                    tx_power_real = twoscmp(int(tx_power, 16))
                    # Transformamos el mayor a entero
                    major_int = int(major, 16)
                    major_f = major_int/100 # bme688
                    # Transformamos el menor a entero
                    minor_int = int(minor,16)
                    minor_f = minor_int/100 # bme688, it is divided by 10 initially in the dialog's firmware.
                    print("Temperature: {} C, Humidity: {} %r.H.".format(major_f, minor_f), time.time())
                    # Llamamos a la funcion para obtener la calidad del aire
                    air_quality_score(minor_f, air)
                    print("")
    else:
        time.sleep(0.050)