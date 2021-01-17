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
    return render_template("homepage.html")

@app.route("/routes/<int:route_id>", methods=['GET'])
def route(route_id):
    db = Database()
    route = db.get_route(route_id)
    user = db.get_user(route.userid)
    return render_template("route.html", route = route, user = user)

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
    db = Database()
    activities = db.get_all_activities()
    return render_template("new_route.html", activities = activities)

@app.route("/newroute", methods=['POST'])
def newroute_post():
    name = request.form.get("name")
    description = request.form.get("description")
    activities = request.form.getlist("activities")
    userid = request.form.get("userid")
    try:
        with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO routes (user_id, name, description) VALUES (%s, %s, %s)"
            data = [userid, name, description]
            cursor.execute(statement, data)
            for activity in activities:
                statement = "SELECT id FROM routes WHERE user_id = %s AND name = %s AND description = %s"
                data = [userid, name, description]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                statement = "INSERT INTO route_activities (activity_id, route_id) VALUES (%s, %s)"
                data = [activity, value[0]]
                cursor.execute(statement, data)
            cursor.close()
    except Exception as err:
        print("Add route error: ", err)

    return redirect(url_for('routes'))

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
