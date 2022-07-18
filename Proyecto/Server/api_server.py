import datetime
import requests

from crypt import methods
from re import M, T
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
    pressure = db.Column(db.Integer)

    def __init__(self, nodo, iteration, year, month, day, lightB, lightR, humidity, temperature, pressure):
        self.nodo = nodo
        self.iteration = iteration
        self.year = year
        self.month = month
        self.day = day
        self.lightB = lightB
        self.lightR = lightR
        self.humidity = humidity
        self.temperature = temperature
        self.pressure = pressure

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nodo', 'iteration', 'year', 'month', 'day', 'lightB', 'lightR', 'humidity', 'temperature', 'pressure')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/aula_600')
def aula_600():
    temp_data_day = []
    temp_label_day = []
    temp_data_month = []
    temp_label_month = []
    hum_data_day = []
    hum_label_day = []
    hum_data_month = []
    hum_label_month = []
    press_data_day = []
    press_label_day = []
    press_data_month = []
    press_label_month = []
    
    actual_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-last/1')
    
    temp_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/1/temperature')
    for dic in temp_day.json():
        for key,value in dic.items():
            temp_label_day.append('')
            aux = round(value,2)
            temp_data_day.append(aux)
    temp_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/1/temperature')
    for dic in temp_month.json():
        for key,value in dic.items():
            temp_label_month.append('')
            aux = round(value,2)
            temp_data_month.append(aux)
    
    hum_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/1/humidity')
    for dic in hum_day.json():
        for key,value in dic.items():
            hum_label_day.append('')
            aux = round(value,2)
            hum_data_day.append(aux)
    hum_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/1/humidity')
    for dic in hum_month.json():
        for key,value in dic.items():
            hum_label_month.append('')
            aux = round(value,2)
            hum_data_month.append(aux)

    press_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/1/pressure')
    for dic in press_day.json():
        for key,value in dic.items():
            press_label_day.append('')
            aux = round(value/1000,2)
            press_data_day.append(aux)
    press_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/1/pressure')
    for dic in press_month.json():
        for key,value in dic.items():
            press_label_month.append('')
            aux = round(value/1000,2)
            press_data_month.append(aux)

    max_temp_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/1/temperature')
    aux_temp = max_temp_day.json()
    max_temp_day = round(aux_temp['temperature'] + 3,2)
    max_temp_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/1/temperature')
    aux_temp = max_temp_month.json()
    max_temp_month = round(aux_temp['temperature'] + 3,2)

    max_hum_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/1/humidity')
    aux_hum = max_hum_day.json()
    max_hum_day = round(aux_hum['humidity'] + 3,2)
    max_hum_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/1/humidity')
    aux_hum = max_hum_month.json()
    max_hum_month = round(aux_hum['humidity'] + 3,2)

    max_press_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/1/pressure')
    aux_press = max_press_day.json()
    max_press_day = round(aux_press['pressure'] + 3,2)
    max_press_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/1/pressure')
    aux_press = max_press_month.json()
    max_press_month = round(aux_press['pressure'] + 3,2)

    title_temp_day = 'Temperatura del dia (°C)'
    title_temp_month = 'Temperatura del mes (°C)'
    title_hum_day = 'Humedad Relativa del dia (%RH)'
    title_hum_month = 'Humedad Relativa del mes (%RH)'
    title_press_day = 'Presion del dia (kPA)'
    title_press_month = 'Presion del mes (kPA)'

    return render_template('aula_600.html', 
                            actual_data=actual_data.json(),
                            max_temp_day=max_temp_day, title_temp_day=title_temp_day, labels_temp_day=temp_label_day, values_temp_day=temp_data_day,
                            max_temp_month=max_temp_month, title_temp_month=title_temp_month, labels_temp_month=temp_label_month, values_temp_month=temp_data_month,
                            max_hum_day=max_hum_day, title_hum_day=title_hum_day, labels_hum_day=hum_label_day, values_hum_day=hum_data_day,
                            max_hum_month=max_hum_month, title_hum_month=title_hum_month, labels_hum_month=hum_label_month, values_hum_month=hum_data_month,
                            max_press_day=max_press_day, title_press_day=title_press_day, labels_press_day=press_label_day, values_press_day=press_data_day,
                            max_press_month=max_press_month, title_press_month=title_press_month, labels_press_month=press_label_month, values_press_month=press_data_month
                            )

@app.route("/aula_601", methods=['GET'])
def aula_601():
    temp_data_day = []
    temp_label_day = []
    temp_data_month = []
    temp_label_month = []
    hum_data_day = []
    hum_label_day = []
    hum_data_month = []
    hum_label_month = []
    press_data_day = []
    press_label_day = []
    press_data_month = []
    press_label_month = []
    
    actual_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-last/2')
    
    temp_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/2/temperature')
    for dic in temp_day.json():
        for key,value in dic.items():
            temp_label_day.append('')
            aux = round(value,2)
            temp_data_day.append(aux)
    temp_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/2/temperature')
    for dic in temp_month.json():
        for key,value in dic.items():
            temp_label_month.append('')
            aux = round(value,2)
            temp_data_month.append(aux)
    
    hum_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/2/humidity')
    for dic in hum_day.json():
        for key,value in dic.items():
            hum_label_day.append('')
            aux = round(value,2)
            hum_data_day.append(aux)
    hum_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/2/humidity')
    for dic in hum_month.json():
        for key,value in dic.items():
            hum_label_month.append('')
            aux = round(value,2)
            hum_data_month.append(aux)

    press_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/2/pressure')
    for dic in press_day.json():
        for key,value in dic.items():
            press_label_day.append('')
            aux = round(value/1000,2)
            press_data_day.append(aux)
    press_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/2/pressure')
    for dic in press_month.json():
        for key,value in dic.items():
            press_label_month.append('')
            aux = round(value/1000,2)
            press_data_month.append(aux)

    max_temp_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/2/temperature')
    aux_temp = max_temp_day.json()
    max_temp_day = round(aux_temp['temperature'] + 3,2)
    max_temp_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/2/temperature')
    aux_temp = max_temp_month.json()
    max_temp_month = round(aux_temp['temperature'] + 3,2)

    max_hum_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/2/humidity')
    aux_hum = max_hum_day.json()
    max_hum_day = round(aux_hum['humidity'] + 3,2)
    max_hum_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/2/humidity')
    aux_hum = max_hum_month.json()
    max_hum_month = round(aux_hum['humidity'] + 3,2)

    max_press_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/2/pressure')
    aux_press = max_press_day.json()
    max_press_day = round(aux_press['pressure'] + 3,2)
    max_press_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/2/pressure')
    aux_press = max_press_month.json()
    max_press_month = round(aux_press['pressure'] + 3,2)

    title_temp_day = 'Temperatura del dia (°C)'
    title_temp_month = 'Temperatura del mes (°C)'
    title_hum_day = 'Humedad Relativa del dia (%RH)'
    title_hum_month = 'Humedad Relativa del mes (%RH)'
    title_press_day = 'Presion del dia (kPA)'
    title_press_month = 'Presion del mes (kPA)'

    return render_template('aula_600.html', 
                            actual_data=actual_data.json(),
                            max_temp_day=max_temp_day, title_temp_day=title_temp_day, labels_temp_day=temp_label_day, values_temp_day=temp_data_day,
                            max_temp_month=max_temp_month, title_temp_month=title_temp_month, labels_temp_month=temp_label_month, values_temp_month=temp_data_month,
                            max_hum_day=max_hum_day, title_hum_day=title_hum_day, labels_hum_day=hum_label_day, values_hum_day=hum_data_day,
                            max_hum_month=max_hum_month, title_hum_month=title_hum_month, labels_hum_month=hum_label_month, values_hum_month=hum_data_month,
                            max_press_day=max_press_day, title_press_day=title_press_day, labels_press_day=press_label_day, values_press_day=press_data_day,
                            max_press_month=max_press_month, title_press_month=title_press_month, labels_press_month=press_label_month, values_press_month=press_data_month
                            )

@app.route("/aula_602", methods=['GET'])
def aula_602():
    temp_data_day = []
    temp_label_day = []
    temp_data_month = []
    temp_label_month = []
    hum_data_day = []
    hum_label_day = []
    hum_data_month = []
    hum_label_month = []
    press_data_day = []
    press_label_day = []
    press_data_month = []
    press_label_month = []
    
    actual_data = requests.get('http://' + SERVER_ADDRESS + '/consultation-last/3')
    
    temp_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/3/temperature')
    for dic in temp_day.json():
        for key,value in dic.items():
            temp_label_day.append('')
            aux = round(value,2)
            temp_data_day.append(aux)
    temp_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/3/temperature')
    for dic in temp_month.json():
        for key,value in dic.items():
            temp_label_month.append('')
            aux = round(value,2)
            temp_data_month.append(aux)
    
    hum_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/3/humidity')
    for dic in hum_day.json():
        for key,value in dic.items():
            hum_label_day.append('')
            aux = round(value,2)
            hum_data_day.append(aux)
    hum_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/3/humidity')
    for dic in hum_month.json():
        for key,value in dic.items():
            hum_label_month.append('')
            aux = round(value,2)
            hum_data_month.append(aux)

    press_day = requests.get('http://' + SERVER_ADDRESS + '/consultation-day/3/pressure')
    for dic in press_day.json():
        for key,value in dic.items():
            press_label_day.append('')
            aux = round(value/1000,2)
            press_data_day.append(aux)
    press_month = requests.get('http://' + SERVER_ADDRESS + '/consultation-month/3/pressure')
    for dic in press_month.json():
        for key,value in dic.items():
            press_label_month.append('')
            aux = round(value/1000,2)
            press_data_month.append(aux)

    max_temp_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/3/temperature')
    aux_temp = max_temp_day.json()
    max_temp_day = round(aux_temp['temperature'] + 3,2)
    max_temp_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/3/temperature')
    aux_temp = max_temp_month.json()
    max_temp_month = round(aux_temp['temperature'] + 3,2)

    max_hum_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/3/humidity')
    aux_hum = max_hum_day.json()
    max_hum_day = round(aux_hum['humidity'] + 3,2)
    max_hum_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/3/humidity')
    aux_hum = max_hum_month.json()
    max_hum_month = round(aux_hum['humidity'] + 3,2)

    max_press_day = requests.get('http://' + SERVER_ADDRESS + '/max-day/3/pressure')
    aux_press = max_press_day.json()
    max_press_day = round(aux_press['pressure'] + 3,2)
    max_press_month = requests.get('http://' + SERVER_ADDRESS + '/max-month/3/pressure')
    aux_press = max_press_month.json()
    max_press_month = round(aux_press['pressure'] + 3,2)

    title_temp_day = 'Temperatura del dia (°C)'
    title_temp_month = 'Temperatura del mes (°C)'
    title_hum_day = 'Humedad Relativa del dia (%RH)'
    title_hum_month = 'Humedad Relativa del mes (%RH)'
    title_press_day = 'Presion del dia (kPA)'
    title_press_month = 'Presion del mes (kPA)'

    return render_template('aula_600.html', 
                            actual_data=actual_data.json(),
                            max_temp_day=max_temp_day, title_temp_day=title_temp_day, labels_temp_day=temp_label_day, values_temp_day=temp_data_day,
                            max_temp_month=max_temp_month, title_temp_month=title_temp_month, labels_temp_month=temp_label_month, values_temp_month=temp_data_month,
                            max_hum_day=max_hum_day, title_hum_day=title_hum_day, labels_hum_day=hum_label_day, values_hum_day=hum_data_day,
                            max_hum_month=max_hum_month, title_hum_month=title_hum_month, labels_hum_month=hum_label_month, values_hum_month=hum_data_month,
                            max_press_day=max_press_day, title_press_day=title_press_day, labels_press_day=press_label_day, values_press_day=press_data_day,
                            max_press_month=max_press_month, title_press_month=title_press_month, labels_press_month=press_label_month, values_press_month=press_data_month
                            )

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
    pressure = information['pressure']

    new_task = Task(nodo, iteration, year, month, day, lightB, lightR, humidity, temperature, pressure)

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

@app.route('/consultation-month/<id>/<arg>', methods=['GET'])
def consutation_month(id, arg):
    global YEAR, MONTH
    requests.get('http://' + SERVER_ADDRESS + '/time')
    if arg == "temperature":
        task = db.session.query(Task.temperature).filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).order_by(Task.day.asc()).all()
    if arg == "humidity":
        task = db.session.query(Task.humidity).filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).all()
    if arg == "pressure":
        task = db.session.query(Task.pressure).filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).all()
    
    resul = tasks_schema.dump(task)
    return jsonify(resul)

@app.route('/consultation-day/<id>/<arg>', methods=['GET'])
def consutation_day(id,arg):
    global YEAR, MONTH, DAY
    requests.get('http://' + SERVER_ADDRESS + '/time')
    if arg == "temperature":
        task = db.session.query(Task.temperature).filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).all()
    if arg == "humidity":
        task = db.session.query(Task.humidity).filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).all()
    if arg == "pressure":
        task = db.session.query(Task.pressure).filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).all()
    
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

@app.route('/max-day/<id>/<arg>')
def maxDay(id,arg):
    global YEAR, MONTH, DAY
    requests.get('http://' + SERVER_ADDRESS + '/time')
    if arg == "temperature":
        task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).order_by(Task.temperature.desc()).first()
    if arg == "pressure":
        task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).order_by(Task.pressure.desc()).first()
    if arg == "humidity":
        task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).order_by(Task.humidity.desc()).first()
    resul = task_schema.dump(task)
    iter = resul['{}'.format(str(arg))]
    if arg == "pressure":
        iter = round(iter/1000,2)
    return jsonify({'{}'.format(str(arg)) : iter})

@app.route('/max-month/<id>/<arg>')
def maxmonth(id,arg):
    global YEAR, MONTH
    requests.get('http://' + SERVER_ADDRESS + '/time')
    if arg == "temperature":
        task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).order_by(Task.temperature.desc()).first()
    if arg == "pressure":
        task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).order_by(Task.pressure.desc()).first()
    if arg == "humidity":
        task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).order_by(Task.humidity.desc()).first()
    resul = task_schema.dump(task)
    iter = resul['{}'.format(str(arg))]
    if arg == "pressure":
        iter = round(iter/1000,2)
    return jsonify({'{}'.format(str(arg)) : iter})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)