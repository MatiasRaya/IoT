from flask import Flask, redirect, render_template, request

app = Flask(__name__)

sensor = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sensores")
def sensores():
    return render_template("sensores.html")

if __name__ == "__main__":
    app.run(debug=True)