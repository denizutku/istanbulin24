from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, LoginManager

import psycopg2
from models.database import Database
from models.user import User
from models.route import Route
from models.activity import Activity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
lm = LoginManager()
lm.init_app(app)
# lm.login_view("login")

@lm.user_loader
def load_user(user_id):
    db = Database()
    return db.get_user(user_id)

@app.route("/")
def homepage():
    user = User(id="0",username="test",password="test",name="test",surname="test",email="test")
    db = Database()
    db.add_user(user)
    # usertest = db.get_user(0)
    # print(usertest.email)
    return render_template("homepage.html")

@app.route("/routes")
def routes():
    route = Route(id="0", userid="0",name="test route", description="test description")
    db = Database()
    db.add_route(route)
    routetest = db.get_route(0)
    print(routetest.description)
    return render_template("routes.html")

@app.route("/newroute")
def newroute():
    return render_template("new_route.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    db = Database()
    user = db.get_user_by_username(username)
    
    if not user:
        print(username)
        flash('Wrong!')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('homepage'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
