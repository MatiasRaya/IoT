from cProfile import label
from calendar import month
import datetime
from optparse import Values
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

# @app.route("/aula_600", methods=['GET'])
# def aula_600():
#     temp1 = []
#     temp2 = []
#     label_day = []
#     data_day = []
#     temperature_day = {}
#     temperature_month = {}
#     i = 0
#     j = 0
#     actual_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-last/1')
#     month_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/1')
#     day_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/1')
#     for dic in day_data.json():
#         for key, value in dic.items():
#                 if key == 'temperature':
#                     temp1.append(value)
#                     data_day.append(value)
#                     label_day.append('temperature{:0}'.format(i))
#                     temperature_day.update({'temperature{:0}'.format(i) : value})
#                     i += 1
#     for dic in month_data.json():
#         for key, value in dic.items():
#                 if key == 'temperature':
#                     temp2.append(value)
#                     temperature_month.update({'temperature{:0}'.format(j) : value})
#                     labels.append('temperature{:0}'.format(j))
#                     data.append(value)
#                     j += 1
#     print(len(temperature_day))
#     print(len(temperature_month))
#     print(len(temp1+temp2))
#     print(label_day)
#     print()
#     print(data_day)
#     return render_template("aula_600.html", actual_data=actual_data.json(), labels=label_day, values=data_day)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

@app.route('/aula_600')
def aula_600():
    line_labels=labels
    line_values=values

    temp1 = []
    temp2 = []
    label_day = []
    data_day = []
    temperature_day = {}
    temperature_month = {}
    i = 0
    j = 0
    actual_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-last/1')
    month_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/1')
    day_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/1')
    for dic in day_data.json():
        for key, value in dic.items():
                if key == 'temperature':
                    temp1.append(value)
                    data_day.append(value)
                    label_day.append('temperature{:0}'.format(i))
                    temperature_day.update({'temperature{:0}'.format(i) : value})
                    i += 1
    return render_template('aula_600.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)

@app.route("/aula_601", methods=['GET'])
def aula_601():
    return render_template("aula_601.html")

@app.route("/aula_602", methods=['GET'])
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

@app.route('/consultation-day/<id>', methods=['GET'])
def consutation_day(id):
    global DAY
    requests.get('http://' + SERVER_ADDRESS + '/time')
    task = Task.query.filter(Task.nodo==id, Task.day==DAY)
    resul = tasks_schema.dump(task)
    return jsonify(resul)

@app.route('/consultation-month/<id>', methods=['GET'])
def consutation_month(id):
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