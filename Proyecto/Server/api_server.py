from calendar import month
import datetime

from crypt import methods
from re import M
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos-ambientales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

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

    def __init__(self, nodo, iteration, year, month, day, lightB, lightR, humidity, temperature, altitude):
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

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nodo', 'iteration', 'year', 'month', 'day', 'lightB', 'lightR', 'humidity', 'temperature', 'altitude')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

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

    new_task = Task(nodo, iteration, year, month, day, lightB, lightR, humidity, temperature, altitude)

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

@app.route('/consultation-first/<id>', methods=['GET'])
def consutation_first(id):
    task = Task.query.filter(Task.nodo==id).order_by(Task.id.asc()).first()
    resul = task_schema.dump(task)
    return jsonify(resul)

@app.route('/time', methods=['GET'])
def time():
    x = datetime.datetime.now()
    year = x.year
    month = x.month
    day = x.day
    return jsonify({
        'year' : year,
        'month' : month,
        'day' : day
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