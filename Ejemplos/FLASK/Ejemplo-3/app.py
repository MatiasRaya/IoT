from crypt import methods
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/person", methods=['POST', 'GET'])
def handle_person():
    if request.method == 'POST':
        return "Se recibió un POST"
    else:
        return "Se recibió un GET"

@app.route("/persons")
def persons():
    person1 = {
        "name": "Bob"
    }
    return jsonify(person1)

@app.route("/error")
def error():
    contenido = {
        "detalles": "Hubo un error en la solicitud"
    }
    resp = jsonify(contenido)
    resp.status_code = 400
    return resp

@app.route("/errors")
def errors():
    contenido = {
        "detalles": "Hubo un error en la solicitud"
    }
    return jsonify(contenido), 400

@app.route("/data", methods=['POST'])
def get_data():
    print('Holaaaaa')
    try:
        json = request.get_json(force=True)
        print(json)
    except:
        print('error handleado')
    
    return "Hola"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)