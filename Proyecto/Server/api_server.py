from crypt import methods
import json
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
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    altitude = db.Column(db.Integer)

    def __init__(self, nodo, humidity, temperature, altitude):
        self.nodo = nodo
        self.humidity = humidity
        self.temperature = temperature
        self.altitude = altitude

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nodo', 'humidity', 'temperature', 'altitude')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/data', methods=['POST'])
def create_data():
    information = request.get_json(force=True)
    nodo = information['nodo']
    humidity = information['humidity']
    temperature = information['temperature']
    altitude = information['altitude']

    new_task = Task(nodo, humidity, temperature, altitude)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'value' : 'key'})

@app.route('/consultation/<id>', methods=['GET'])
def create_consult(id):
    all_tasks = Task.query.filter_by(nodo=id).all()
    result = tasks_schema.dump(all_tasks)
    size = len(result)
    print(size)
    return jsonify(result),len(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)