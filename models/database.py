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


    ##USER

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
        
    def get_user(self,id):
        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "SELECT id, username, password, name, surname, email FROM users WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                user = User(value[0], value[1], value[2], value[3], value[4], value[5])
                return user
        except Exception as err:
            print("Get user error: ", err)
        
        return None

    def delete_user(self,id):
        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM users WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Delete user error: ", err)

    def update_user(self, id, attributes, values):
        attributes_table = {
            "username": "username",
            "password": "password",
            "name": "name",
            "surname": "surname",
            "email": "email",
        }

        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "UPDATE users SET "
                for i in range(len(attributes) - 1):
                    statement += attributes_table[attributes[i]] + " = %s ,"
                statement += attributes_table[attributes[-1]] + " = %s WHERE id = %s"
                values.append(id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update user error: ", err)



    ##ROUTE

    def add_route(self, route):
        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO routes (id, userid, name, description) VALUES (%s, %s, %s, %s)"
                data = [route.id, route.userid, route.name, route.description]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add route error: ", err)
        
        return route
        
    def get_route(self,id):
        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "SELECT id, user_id, name, description FROM routes WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                route = Route(value[0], value[1], value[2], value[3])
                return route
        except Exception as err:
            print("Get route error: ", err)
        
        return None

    def delete_route(self,id):
        try:
            with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM routes WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Delete user error: ", err)

    # def update_route(self, id, attributes, values):
    #     attributes_table = {
    #         "name": "name",
    #         "description": "description",
    #     }

    #     try:
    #         with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
    #             cursor = connection.cursor()
    #             statement = "UPDATE routes SET "
    #             for i in range(len(attributes) - 1):
    #                 statement += attributes_table[attributes[i]] + " = %s ,"
    #             statement += attributes_table[attributes[-1]] + " = %s WHERE id = %s"
    #             values.append(id)
    #             cursor.execute(statement, values)
    #             cursor.close()
    #     except Exception as err:
    #         print("Update user error: ", err)
    