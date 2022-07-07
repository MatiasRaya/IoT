from calendar import month
import datetime
import requests

from crypt import methods
from re import M
from urllib import response
from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos-ambientales.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

DAY = 0
MONTH = 0
YEAR = 0

SERVER_ADDRESS = '192.168.1.142:5000' #LCD

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nodo = db.Column(db.Integer)
    iteration = db.Column(db.Integer)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    lightB = db.Column(db.Integer)
    lightR = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    altitude = db.Column(db.Integer)
    pressure = db.Column(db.Integer)

    def __init__(self, nodo, iteration, year, month, day, lightB, lightR, humidity, temperature, altitude, pressure):
        self.nodo = nodo
        self.iteration = iteration
        self.year = year
        self.month = month
        self.day = day
        self.lightB = lightB
        self.lightR = lightR
        self.humidity = humidity
        self.temperature = temperature
        self.altitude = altitude
        self.pressure = pressure

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nodo', 'iteration', 'year', 'month', 'day', 'lightB', 'lightR', 'humidity', 'temperature', 'altitude', 'pressure')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/aula_600", methods=['GET'])
def aula_600():
    temperature = []
    actual_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-last/1')
    month_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/1')
    for dic in month_data.json():
        for key, value in dic.items():
                if key == 'temperature':
                    temperature.append(value)
                    print(temperature)
                    print()
    print(len(temperature))
    return render_template("aula_600.html", actual_data=actual_data.json(),temperature=temperature)

@app.route("/aula_601/2")
def aula_601():
    return render_template("aula_601.html")

@app.route("/aula_602")
def aula_602():
    return render_template("aula_602.html")

@app.route('/data', methods=['POST'])
def create_data():
    information = request.get_json(force=True)
    nodo = information['nodo']
    iteration = information['iteration']
    year = information['year']
    month = information['month']
    day = information['day']
    lightB = information['lightB']
    lightR = information['lightR']
    humidity = information['humidity']
    temperature = information['temperature']
    altitude = information['altitude']
    pressure = information['pressure']

    new_task = Task(nodo, iteration, year, month, day, lightB, lightR, humidity, temperature, altitude, pressure)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'key' : 'value'})

@app.route('/consultation-all/<id>', methods=['GET'])
def consultation_all(id):
    all_tasks = Task.query.filter_by(nodo=id).all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/consultation-last/<id>', methods=['GET'])
def consutation_last(id):
    task = Task.query.filter(Task.nodo==id).order_by(Task.id.desc()).first()
    resul = task_schema.dump(task)
    return jsonify(resul)

@app.route('/consultation-month/<id>', methods=['GET'])
def consutation_first(id):
    global MONTH
    requests.get('http://' + SERVER_ADDRESS + '/time')
    task = Task.query.filter(Task.nodo==id, Task.month==MONTH)
    resul = tasks_schema.dump(task)
    return jsonify(resul)

@app.route('/time', methods=['GET'])
def time():
    global DAY, MONTH, YEAR
    x = datetime.datetime.now()
    YEAR = x.year
    MONTH = x.month
    DAY = x.day
    return jsonify({
        'year' : YEAR,
        'month' : MONTH,
        'day' : DAY
    })

@app.route('/iteration/<id>', methods=['GET'])
def itertaio(id):
    task = Task.query.filter(Task.nodo==id).order_by(Task.id.desc()).first()
    resul = task_schema.dump(task)
    iter = resul['iteration']
    return jsonify({'iteration' : iter})

@app.route('/delete/<id>', methods=['GET'])
def delte_table(id):
    db.session.query(Task).filter(Task.nodo==id).delete()
    db.session.commit()
    return jsonify({'key' : 'value'})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)