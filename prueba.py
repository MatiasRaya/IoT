from unittest import result

import urequests
respuesta = {
    "status": True,
    "result": [
        {
            "id": "631a8d224f4d200011f9f3c1",
            "time": "2022-09-09T00:47:30.826Z",
            "value": "1",
            "variable": "actualization2",
            "group": "1662684450433",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8d224f4d200011f9f3c0",
            "time": "2022-09-09T00:47:30.825Z",
            "value": "5",
            "variable": "actuaization1",
            "group": "1662684450433",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038cc",
            "time": "2022-09-09T00:44:30.438Z",
            "value": "232505064286148",
            "variable": "location232505064286148",
            "location": {
                "type": "Point",
                "coordinates": [
                    0,
                    0
                ]
            },
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038cb",
            "time": "2022-09-09T00:44:30.438Z",
            "value": -25,
            "variable": "rssi232505064286148",
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038ca",
            "time": "2022-09-09T00:44:30.438Z",
            "value": 97.25,
            "variable": "voc232505064286148",
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038c9",
            "time": "2022-09-09T00:44:30.437Z",
            "value": 25122,
            "variable": "gas_resistance232505064286148",
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038c8",
            "time": "2022-09-09T00:44:30.437Z",
            "value": 35.6,
            "variable": "humidity232505064286148",
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038c7",
            "time": "2022-09-09T00:44:30.436Z",
            "value": 967,
            "variable": "pressure232505064286148",
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c6e7c242a00185038c6",
            "time": "2022-09-09T00:44:30.436Z",
            "value": 21.97,
            "variable": "temperature232505064286148",
            "group": "5c83058100a242c7e6c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c64b9d0fa0018f4c017",
            "time": "2022-09-09T00:44:20.638Z",
            "value": "232505064286148",
            "variable": "location232505064286148",
            "location": {
                "type": "Point",
                "coordinates": [
                    0,
                    0
                ]
            },
            "group": "010c4f8100af0d9b46c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c64b9d0fa0018f4c016",
            "time": "2022-09-09T00:44:20.637Z",
            "value": -25,
            "variable": "rssi232505064286148",
            "group": "010c4f8100af0d9b46c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c64b9d0fa0018f4c015",
            "time": "2022-09-09T00:44:20.637Z",
            "value": 96.2,
            "variable": "voc232505064286148",
            "group": "010c4f8100af0d9b46c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c64b9d0fa0018f4c014",
            "time": "2022-09-09T00:44:20.637Z",
            "value": 25196,
            "variable": "gas_resistance232505064286148",
            "group": "010c4f8100af0d9b46c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c64b9d0fa0018f4c013",
            "time": "2022-09-09T00:44:20.635Z",
            "value": 33.92,
            "variable": "humidity232505064286148",
            "group": "010c4f8100af0d9b46c8a136",
            "device": "6317aafdb94d290011b199f9"
        },
        {
            "id": "631a8c64b9d0fa0018f4c012",
            "time": "2022-09-09T00:44:20.635Z",
            "value": 967,
            "variable": "pressure232505064286148",
            "group": "010c4f8100af0d9b46c8a136",
            "device": "6317aafdb94d290011b199f9"
        }
    ]
}
SERVER_ADDRESS = "https://api.tago.io/data"
headers={'Authorization':'531bc5a5-4e7b-433d-9f32-e605ac4e8a15'}
print((urequests.get(SERVER_ADDRESS,headers=headers))["result"])
# pe = list(filter(lambda actual: actual["variable"] == "actuaization1", list(filter(lambda actual: actual["variable"] == "actuaization1",(requests.get(SERVER_ADDRESS,headers=headers))["result"]))[0]["value"]
# prue = (respuesta["result"])
# print((respuesta["result"]))
# print(len(respuesta["result"]))
# print(respuesta["result"][len(respuesta["result"])-1])
# print(list(filter(lambda actual: actual["variable"] == "actuaization1", prue)))
# pr = list(filter(lambda actual: actual["variable"] == "actuaization1", respuesta["result"]))
# print(type(pr))
# print(pr)
p = list(filter(lambda actual: actual["variable"] == "actuaization1", list(filter(lambda actual: actual["variable"] == "actuaization1", respuesta["result"]))))[0]["value"]
print(p)
