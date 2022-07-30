import datetime
import os

from flask import Flask, request, jsonify, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from geopy.geocoders import Nominatim
from geopy.point import Point

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

SECOND = 0
MINUTE = 0
HOUR = 0
DAY = 0
MONTH = 0
YEAR = 0
TRANSMITION1 = 5
SENSORS1 = 1
TRANSMITION2 = 5
SENSORS2 = 1
TRANSMITION3 = 5
SENSORS3 = 1
MULT1 = 1
MULT2 = 1
MULT3 = 1
BIG = 5

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nodo = db.Column(db.Integer)
    iteration = db.Column(db.Integer)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    second = db.Column(db.Integer)
    posLat = db.Column(db.Integer)
    posLon = db.Column(db.Integer)
    ubication = db.Column(db.String)

    def __init__(self, nodo, iteration, year, month, day, hour, minute, second, posLat, posLon, ubication):
        self.nodo = nodo
        self.iteration = iteration
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.posLat = posLat
        self.posLon = posLon
        self.ubication = ubication

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nodo', 'iteration', 'year', 'month', 'day', 'hour', 'minute', 'second', 'posLat', 'posLon', 'ubication')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

def big_transmition():
    global BIG
    param1 = int(TRANSMITION1)
    param2 = int(TRANSMITION2)
    param3 = int(TRANSMITION3)
    if(param1 > param2 and param1 > param3):
        BIG = param1
    elif(param2 > param3 and param2 > param1):
        BIG = param2
    elif(param3 > param1 and param3 > param2):
        BIG = param3

def time():
    global SECOND, MINUTE, HOUR, DAY, MONTH, YEAR
    x = datetime.datetime.now()
    YEAR = x.year
    MONTH = x.month
    DAY = x.day
    HOUR = x.hour
    MINUTE = x.minute
    SECOND = x.second

def consultation_last(id):
    time()
    tasks = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).order_by(Task.id.desc()).first()
    resul1 = task_schema.dump(tasks)
    return jsonify(resul1)    

def consultation_all(id):
    task = Task.query.filter(Task.nodo==id).order_by(Task.id.desc()).all()
    resul = tasks_schema.dump(task)
    return jsonify(resul)

def consultation_day(id):
    time()
    task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH, Task.day==DAY).order_by(Task.id.desc()).all()
    resul = tasks_schema.dump(task)
    return jsonify(resul)

def consultation_month(id):
    time()
    task = Task.query.filter(Task.nodo==id, Task.year==YEAR, Task.month==MONTH).order_by(Task.id.desc()).all()
    resul = tasks_schema.dump(task)
    return jsonify(resul)

def consultation_year(id):
    time()
    task = Task.query.filter(Task.nodo==id, Task.year==YEAR).order_by(Task.id.desc()).all()
    resul = tasks_schema.dump(task)
    return jsonify(resul)

def consultation_ubication(lat,long):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.reverse("{}, {}".format(lat,long))
    return location.address

@app.route('/')
def home():
    actual_data_1 = []
    actual_data_2 = []
    actual_data_3 = []

    actual_data1 = consultation_last(id=1)
    actual_data1 = actual_data1.json
    for key,value in actual_data1.items():
        if key != "id" and key != "nodo" and key != "iteration":
            actual_data_1.append(value)
    print(actual_data_1)
    
    actual_data2 = consultation_last(id=2)
    actual_data2 = actual_data2.json
    for key,value in actual_data2.items():
        if key != "id" and key != "nodo" and key != "iteration":
            actual_data_2.append(value)
    
    actual_data3 = consultation_last(id=3)
    actual_data3 = actual_data3.json
    for key,value in actual_data3.items():
        if key != "id" and key != "nodo" and key != "iteration":
            actual_data_3.append(value)
    big_transmition()
    return render_template("index.html", actual=BIG+2,
                           actual_data1=actual_data_1,
                           actual_data2=actual_data_2,
                           actual_data3=actual_data_3,
                           )

@app.route('/machine/<id>')
def machine(id):
    actual_data_machine = []

    actual_data = consultation_last(id=id)
    actual_data = actual_data.json
    for key,value in actual_data.items():
        if key != "id" and key != "nodo" and key != "iteration":
            actual_data_machine.append(value)

    all_data_all = consultation_all(id=id)
    all_data_all = all_data_all.json

    all_data_day = consultation_day(id=id)
    all_data_day = all_data_day.json

    all_data_month = consultation_month(id=id)
    all_data_month = all_data_month.json

    all_data_year = consultation_year(id=id)
    all_data_year = all_data_year.json

    global BIG
    if(int(id) == 1):
        BIG = int(TRANSMITION1)*int(MULT1)
    elif(int(id) == 2):
        BIG = int(TRANSMITION2)*int(MULT2)
    elif(int(id) == 3):
        BIG = int(TRANSMITION3)*int(MULT3)

    return render_template('machine.html', machine_name=str(id),
                            actual=str(int(BIG)+2),
                            actual_data=actual_data_machine,
                            history_data_all=all_data_all,
                            len_data_all=len(all_data_all),
                            history_data_day=all_data_day,
                            len_data_day=len(all_data_day),
                            history_data_month=all_data_month,
                            len_data_month=len(all_data_month),
                            history_data_year=all_data_year,
                            len_data_year=len(all_data_year),
                            )

@app.route("/rate", methods=['GET','POST'])
def rate():
    return render_template('rate.html')

@app.route("/form/<id>", methods=['POST'])
def form_consul(id):
    global TRANSMITION1, SENSORS1, TRANSMITION2, SENSORS2, TRANSMITION3, SENSORS3, MULT1, MULT2, MULT3
    if int(id) == 1:
        TRANSMITION1 = request.form['transmition']
        SENSORS1 = request.form['sensor']
        MULT1 = request.form['mult']
        return redirect(url_for('rate'))
    if int(id) == 2:
        TRANSMITION2 = request.form['transmition']
        SENSORS2 = request.form['sensor']
        MULT2 = request.form['mult']
        return redirect(url_for('rate'))
    if int(id) == 3:
        TRANSMITION3 = request.form['transmition']
        SENSORS3 = request.form['sensor']
        MULT3 = request.form['mult']
        return redirect(url_for('rate'))
    return id

@app.route('/actualization/<id>', methods=['GET'])
def actualization(id):
    global TRANSMITION1, SENSORS1, TRANSMITION2, SENSORS2, TRANSMITION3, SENSORS3
    if int(id) == 1:
        TRANSMITION1 = int(TRANSMITION1)*int(MULT1)
        SENSORS1 = int(SENSORS1)*int(MULT1)
        return jsonify({
            'transmition' : TRANSMITION1,
            'sensor' : SENSORS1,
            'mult' : MULT1,
        })
    if int(id) == 2:
        TRANSMITION2 = int(TRANSMITION2)*int(MULT2)
        SENSORS2 = int(SENSORS2)*int(MULT2)
        return jsonify({
            'transmition' : TRANSMITION2,
            'sensor' : SENSORS2,
            'mult' : MULT2,
        })
    if int(id) == 3:
        TRANSMITION3 = int(TRANSMITION3)*int(MULT3)
        SENSORS3 = int(SENSORS3)*int(MULT3)
        return jsonify({
            'transmition' : TRANSMITION3,
            'sensor' : SENSORS3,
            'mult' : MULT3,
        })

@app.route('/data', methods=['POST'])
def create_data():
    information = request.get_json(force=True)
    if str(information['posLat']) != "None" and str(information['posLon']) != "None":
        time()
        nodo = information['nodo']
        iteration = information['iteration']
        year = YEAR
        month = MONTH
        day = DAY
        hour = HOUR
        minute = MINUTE
        second = SECOND
        posLat = information['posLat']
        posLon = information['posLon']
        ubication = consultation_ubication(lat=posLat, long=posLon)

        new_task = Task(nodo=nodo, iteration=iteration, year=year, month=month, day=day, hour=hour, minute=minute, second=second, posLat=posLat, posLon=posLon, ubication=ubication)

        db.session.add(new_task)
        db.session.commit()

    return jsonify({'key' : 'value'})

@app.route('/iteration/<id>', methods=['GET'])
def itertaio(id):
    task = Task.query.filter(Task.nodo==id).order_by(Task.id.desc()).first()
    resul = task_schema.dump(task)
    iter = resul['iteration']
    return jsonify({'iteration' : iter})

@app.route('/delete', methods=['GET'])
def delte_table(id):
    db.session.query(Task).delete()
    db.session.commit()
    return jsonify({'key' : 'value'})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
