from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user

import psycopg2 as dbapi2
import os

from base64 import b64encode
from passlib.hash import pbkdf2_sha256 as hasher
from models.database import Database
from models.user import User
from models.route import Route
from models.activity import Activity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
lm = LoginManager()
lm.init_app(app)
url = os.environ.get("DATABASE_URL")

@lm.user_loader
def load_user(user_id):
    db = Database(url)
    return db.get_user(user_id)

@app.route("/")
def homepage():
    db = Database(url)
    routes = db.get_all_routes()
    for i in range(len(routes)):
        user_id = routes[i][1]
        username = db.get_username_by_id(user_id)
        routes[i] = routes[i] + username
    return render_template("homepage.html", routes = routes)

@app.route("/routes/<int:route_id>", methods=['GET'])
def route(route_id):
    db = Database(url)
    route = db.get_route(route_id)
    user = db.get_user(route.user_id)
    activities = db.get_route_activities(route_id)
    score = db.get_route_score(route_id)
    img = None
    is_rated_by_curr_user = db.check_user_rated_route(route_id, current_user.id)
    if route.img_url is not None:
        img = b64encode(route.img_url).decode("UTF-8'")
    return render_template("route.html", route = route, user = user, activities = activities,
     img = img, is_rated = is_rated_by_curr_user, score = score)

@app.route("/routes")
def routes():
    db = Database(url)
    routes = db.get_all_routes()
    for i in range(len(routes)):
        user_id = routes[i][1]
        username = db.get_username_by_id(user_id)
        routes[i] = routes[i] + username
    return render_template("routes.html", routes = routes)

@app.route("/newroute")
def newroute():
    db = Database(url)
    activities = db.get_all_activities()
    return render_template("new_route.html", activities = activities)

@app.route("/newroute", methods=['POST'])
def newroute_post():
    name = request.form.get("name")
    description = request.form.get("description")
    activities = request.form.getlist("activities")
    userid = request.form.get("userid")
    img_url = request.files["photo"]

    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO routes (user_id, name, description, img_url) VALUES (%s, %s, %s, %s)"
            data = [userid, name, description, img_url.read()]
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

@app.route("/routes/<int:route_id>/update", methods=['GET'])
def route_update(route_id):
    db = Database(url)
    route = db.get_route(route_id)
    user = db.get_user(route.user_id)
    activities = db.get_all_activities()
    img = None
    if route.img_url is not None:
        img = b64encode(route.img_url).decode("UTF-8'")
    return render_template("route_update.html", route = route, user = user, activities = activities, img = img)

@app.route("/routes/<int:route_id>/updateroute", methods=['POST'])
def route_update_save(route_id):
    name = request.form.get("name")
    description = request.form.get("description")
    activities = request.form.getlist("activities")
    userid = request.form.get("userid")
    img_url = request.files["photo"]

    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = "UPDATE routes SET user_id = %s, name = %s, description = %s , img_url = %s WHERE id = %s"
            data = [userid, name, description, img_url.read(),route_id]
            cursor.execute(statement, data)

            statement = "DELETE FROM route_activities WHERE route_id = %s"
            data = [route_id]
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

    return redirect(url_for('route', route_id = route_id))

@app.route("/routes/<int:route_id>/delete")
def route_delete(route_id):
    db = Database(url)
    route = db.delete_route(route_id)
    return redirect(url_for('routes'))

@app.route("/routes/<int:route_id>", methods=["POST"])
def route_rate(route_id):
    score = request.form.get("rate")
    user_id = request.form.get("user_id")
    db = Database(url)
    db.rate_route(route_id,user_id,score)
    return redirect(url_for('route', route_id = route_id))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    db = Database(url)
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
    img_url = request.files["photo"]

    db = Database(url)
    user = db.get_user_by_username(username)

    if user:
        flash('Username already exists.')
        return redirect(url_for('register'))

    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO users (username, password, name, surname, email, img_url, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = [username, hasher.hash(password), name, surname, email, img_url.read(), False]
            cursor.execute(statement, data)
            cursor.close()
    except Exception as err:
        print("Add user error: ", err)

    return redirect(url_for('login'))


@app.route("/users/<int:user_id>", methods=['GET'])
def user(user_id):
    db = Database(url)
    user = db.get_user(user_id)
    img = None
    is_admin = db.is_user_admin(current_user.id)
    if user.img_url is not None:
        img = b64encode(user.img_url).decode("UTF-8'")
    routes = db.get_routes_by_userid(user_id)
    return render_template("user.html", user = user, routes = routes, img = img, is_admin = is_admin)


@app.route("/users/<int:user_id>/update", methods=['GET'])
def user_update(user_id):
    db = Database(url)
    user = db.get_user(user_id)
    img = None
    if user.img_url is not None:
        img = b64encode(user.img_url).decode("UTF-8'")
    routes = db.get_routes_by_userid(user_id)
    return render_template("user_update.html", user = user, routes = routes, img = img)

@app.route("/users/<int:user_id>/updateuser", methods=['POST'])
def user_update_save(user_id):
    username = request.form.get("username")
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    img_url = request.files["photo"]

    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = "UPDATE users SET username = %s, name = %s, surname =%s, email = %s, img_url =%s WHERE id = %s"
            data = [username, name, surname, email, img_url.read(), user_id]
            cursor.execute(statement, data)
            cursor.close()
    except Exception as err:
        print("Add user error: ", err)

    return redirect(url_for('user', user_id = user_id))

@app.route("/users")
def users():
    db = Database(url)
    users = db.get_all_users()
    is_admin = db.is_user_admin(current_user.id)
    return render_template("users.html", users = users, is_admin = is_admin)

@app.route("/users/<int:user_id>/delete", methods=['GET'])
def delete_user(user_id):
    db = Database()
    db.delete_user(user_id)
    return redirect(url_for('users'))

if __name__ == "__main__":
    app.run()
