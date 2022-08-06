from network import LTE
import time
import socket

lte = LTE()

# Seteamos la banda en la que vamos a operar (la cual depende de la version de nuestra FiPy, las basicas son: 3, 4, 12, 13, 20, 28) y la apn del operador de nuestra SIM
# APN para android
# APN Personal: datos.personal.com
# APN Claro: igprs.claro.com.ar
# APN Movistar: wap.gprs.unifon.com.ar //// internet.gprs.unifon.com.ar //// mms.gprs.unifon.com.ar
# APN ios
# APN Personal: datos.personal.com
# APN Claro: igprs.claro.com.ar
# APN Movistar: gprs.unifon.com.ar
# Bandas de 4G LTE en Argentina: 2, 4, 5, 7, 8, 28, 66

# Hailitamos la funcionalidad de radio y conectarse a la red LTE autorizada por la tarjeta SIM
lte.attach(band=28, apn="datos.personal.com")
# lte.attach(band=28, apn="igprs.claro.com.ar")
print("attaching..",end='')
# Consultamos si estamos conectados a la red
while not lte.isattached():
    time.sleep(0.25)
    print('.',end='')
    # Envía un comando AT directamente al módem
    print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
print("attached!")

# Se inicia sesion y se obtiene una direccion IP
lte.connect()
print("connecting [##",end='')
# Consultamos sitenemos una sesion de datos LTE activa y si se ha obtenido ua dirección IP
while not lte.isconnected():
    time.sleep(0.25)
    print('#',end='')
    #print(lte.send_at_cmd('AT!="showphy"'))
    print(lte.send_at_cmd('AT!="fsm"'))
print("] connected!")

# Se traduce el argumento host/port en una secuencia de 5 tuplas qe contengan los argumentos necesarios para crear un socket conectado a ese servicio
print(socket.getaddrinfo('pybytes.pycom.io', 80))  
# Deshabilita completamente el modem LTE, se hace para reducir el consumo de energía al minimo
lte.deinit()