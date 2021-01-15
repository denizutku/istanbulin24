from models.user import User 
from models.route import Route 
from models.activity import Activity 
from models.route_score import Route_Score 
from models.route_activity import Route_Activity 

import psycopg2 as dbapi2

class Database:
    def __init__(self):
        self.users = {}
        self.routes = {}
        self.activities = {}
        # self.url = dbname="postgres",user="postgres",password="1",host="localhost"

    def add_user(self, user):
        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO users (id, username, password, name, surname, email) VALUES (%s, %s, %s, %s, %s, %s)"
                data = [user.id, user.username, user.password, user.name, user.surname, user.email]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add user error: ", err)
        
        return user