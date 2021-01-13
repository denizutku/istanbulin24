from flask import Flask, render_template

import psycopg2


conn = psycopg2.connect(dbname="istanbulin24",user="postgres",password="1",host="localhost")

cursor = conn.cursor()

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/routes")
def routes():
    return render_template("routes.html")

@app.route("/newroute")
def newroute():
    return render_template("new_route.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
