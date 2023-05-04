from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route("/")             #Declaramos un decorador
# def index():
#     nombre = "Matías"
#     apellido = "Raya Plasencia"
#     num = 1
#     lista = [1,2,3,4,5,6,7]
#     return render_template("index.html",nombre=nombre, apellido=apellido, num=num, lista=lista)

# @app.route("/contacto")
# def contacto():
#     return "<h1>Contacto</h1>"

# @app.route("/contacto1")
# def contacto1():
#     return render_template("contacto.html")

# @app.route("/hola/<string:nombre>")
# def hola(nombre):
#     return f"<h1>Hola {nombre}</h1>"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contacto", methods=["POST"])
def contacto():
    nombre = request.form.get("nombre")
    return render_template("contacto.html", nombre=nombre)

if __name__ == "__main__":
    app.run(debug=True)