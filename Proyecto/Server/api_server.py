from crypt import methods
import datetime
import requests

from flask import Flask, request, jsonify, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

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

SERVER_ADDRESS = 'http://192.168.1.142:5000' #LCD

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

@app.route('/')
def home():
    actual_data1 = requests.get(SERVER_ADDRESS + '/consultation-last/1')
    actual_data2 = requests.get(SERVER_ADDRESS + '/consultation-last/2')
    actual_data3 = requests.get(SERVER_ADDRESS + '/consultation-last/3')
    big_transmition()
    return render_template("index.html", actual=BIG+2,
                            actual_data1=actual_data1.json(),
                            actual_data2=actual_data2.json(),
                            actual_data3=actual_data3.json(),
                            )

@app.route('/aula/<name>/<id>')
def aula(name,id):
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
    
    actual_data = requests.get(SERVER_ADDRESS + '/consultation-last/' + id)
    
    temp_day = requests.get(SERVER_ADDRESS + '/consultation-day/' + id + '/temperature')
    for dic in temp_day.json():
        for key,value in dic.items():
            temp_label_day.append('')
            aux = round(value,2)
            temp_data_day.append(aux)
    temp_month = requests.get(SERVER_ADDRESS + '/consultation-month/' + id + '/temperature')
    for dic in temp_month.json():
        for key,value in dic.items():
            temp_label_month.append('')
            aux = round(value,2)
            temp_data_month.append(aux)
    
    hum_day = requests.get(SERVER_ADDRESS + '/consultation-day/' + id + '/humidity')
    for dic in hum_day.json():
        for key,value in dic.items():
            hum_label_day.append('')
            aux = round(value,2)
            hum_data_day.append(aux)
    hum_month = requests.get(SERVER_ADDRESS + '/consultation-month/' + id + '/humidity')
    for dic in hum_month.json():
        for key,value in dic.items():
            hum_label_month.append('')
            aux = round(value,2)
            hum_data_month.append(aux)

    press_day = requests.get(SERVER_ADDRESS + '/consultation-day/' + id + '/pressure')
    for dic in press_day.json():
        for key,value in dic.items():
            press_label_day.append('')
            aux = round(value/1000,2)
            press_data_day.append(aux)
    press_month = requests.get(SERVER_ADDRESS + '/consultation-month/' + id + '/pressure')
    for dic in press_month.json():
        for key,value in dic.items():
            press_label_month.append('')
            aux = round(value/1000,2)
            press_data_month.append(aux)

    max_temp_day = requests.get(SERVER_ADDRESS + '/max-day/' + id + '/temperature')
    aux_temp = max_temp_day.json()
    max_temp_day = round(aux_temp['temperature'] + 3,2)
    max_temp_month = requests.get(SERVER_ADDRESS + '/max-month/' + id + '/temperature')
    aux_temp = max_temp_month.json()
    max_temp_month = round(aux_temp['temperature'] + 3,2)

    max_hum_day = requests.get(SERVER_ADDRESS + '/max-day/' + id + '/humidity')
    aux_hum = max_hum_day.json()
    max_hum_day = round(aux_hum['humidity'] + 3,2)
    max_hum_month = requests.get(SERVER_ADDRESS + '/max-month/' + id + '/humidity')
    aux_hum = max_hum_month.json()
    max_hum_month = round(aux_hum['humidity'] + 3,2)

    max_press_day = requests.get(SERVER_ADDRESS + '/max-day/' + id + '/pressure')
    aux_press = max_press_day.json()
    max_press_day = round(aux_press['pressure'] + 3,2)
    max_press_month = requests.get(SERVER_ADDRESS + '/max-month/' + id + '/pressure')
    aux_press = max_press_month.json()
    max_press_month = round(aux_press['pressure'] + 3,2)

    global BIG
    if(int(id) == 1):
        BIG = int(TRANSMITION1)*int(MULT1)
    elif(int(id) == 2):
        BIG = int(TRANSMITION2)*int(MULT2)
    elif(int(id) == 3):
        BIG = int(TRANSMITION3)*int(MULT3)

    title_temp_day = 'Temperatura del dia (°C)'
    title_temp_month = 'Temperatura del mes (°C)'
    title_hum_day = 'Humedad Relativa del dia (%RH)'
    title_hum_month = 'Humedad Relativa del mes (%RH)'
    title_press_day = 'Presion del dia (kPA)'
    title_press_month = 'Presion del mes (kPA)'

    return render_template('aula.html', aula_name=str(name),
                            actual=str(int(BIG)+2),
                            actual_data=actual_data.json(),
                            max_temp_day=max_temp_day, title_temp_day=title_temp_day, labels_temp_day=temp_label_day, values_temp_day=temp_data_day,
                            max_temp_month=max_temp_month, title_temp_month=title_temp_month, labels_temp_month=temp_label_month, values_temp_month=temp_data_month,
                            max_hum_day=max_hum_day, title_hum_day=title_hum_day, labels_hum_day=hum_label_day, values_hum_day=hum_data_day,
                            max_hum_month=max_hum_month, title_hum_month=title_hum_month, labels_hum_month=hum_label_month, values_hum_month=hum_data_month,
                            max_press_day=max_press_day, title_press_day=title_press_day, labels_press_day=press_label_day, values_press_day=press_data_day,
                            max_press_month=max_press_month, title_press_month=title_press_month, labels_press_month=press_label_month, values_press_month=press_data_month
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
    requests.get(SERVER_ADDRESS + '/time')
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
    requests.get(SERVER_ADDRESS + '/time')
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
    requests.get(SERVER_ADDRESS + '/time')
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
    requests.get(SERVER_ADDRESS + '/time')
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

AUXLAT = 0
AUXLON = 0
COUNTTRACK = 0
@app.route('/track', methods=['POST','GET'])
def track():
    global AUXLAT, AUXLON, COUNTTRACK
    if request.method == "POST":
        information = request.get_json(force=True)
        AUXLAT = information["lat"]
        AUXLON = information["lon"]
        file = open('datos-pytack2.txt','a')
        file.write('Iteracion {}'.format(str(COUNTTRACK)) +'\n' + "{},{}".format(str(AUXLAT),str(AUXLON)) + '\n')
        COUNTTRACK += 1
        file.close()
    else:
        print(AUXLAT)
        print(AUXLON)
    return {"key" : "value"}


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
