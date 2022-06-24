from crypt import methods
from urllib import response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/localadmin/Escritorio/IoT-PS/Ejemplos/FLASK/Ejemplo-6/prueba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    university = db.Column(db.String)

    def __init__(self, name, age, university):
        self.name = name
        self.age = age
        self.university = university

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'university')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks/', methods=['POST'])
def create_task():
    print('START')
    name = request.json['name']
    age = request.json['age']
    university = request.json['university']
    print('TASK')

    new_task = Task(name, age, university)
    print('END TASK')

    db.session.add(new_task)
    db.session.commit()

    print(request.json)
    return jsonify({'key' : 'value'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    # print(request.json['name'])
    return jsonify(result)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    name = request.json['name']
    age = request.json['age']
    university = request.json['university']

    task.name = name
    task.age = age
    task.university = university

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

if __name__ == "__main__":
    app.run(port=5500,debug=True)