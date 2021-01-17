from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
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
    # user = User(id="0",username="test",password=hasher.hash("test"),name="test",surname="test",email="test")
    # db = Database()
    # db.add_user(user)
    # usertest = db.get_user(0)
    # print(usertest.email)
    return render_template("homepage.html")

@app.route("/routes/<int:route_id>", methods=['GET'])
def route(route_id):
    return 'route id %s page' %route_id

@app.route("/routes")
def routes():
    db = Database()
    routes = db.get_all_routes()
    for i in range(len(routes)):
        user_id = routes[i][1]
        username = db.get_username_by_id(user_id)
        routes[i] = routes[i] + username
    return render_template("routes.html", routes = routes)

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

    if not user or not hasher.verify(password, user.password):
        flash('Username or password is wrong. Please try again')
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

@app.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")


    db = Database()
    user = db.get_user_by_username(username)

    if user:
        flash('Username already exists.')
        return redirect(url_for('register'))

    try:
        with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO users (username, password, name, surname, email) VALUES (%s, %s, %s, %s, %s)"
            data = [username, hasher.hash(password), name, surname, email]
            cursor.execute(statement, data)
            cursor.close()
    except Exception as err:
        print("Add user error: ", err)

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
