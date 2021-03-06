from models.user import User 
from models.route import Route 
from models.activity import Activity 
from models.route_score import Route_Score 
from models.route_activity import Route_Activity 

import psycopg2 as dbapi2

class Database:
    def __init__(self, url):
        self.users = {}
        self.routes = {}
        self.activities = {}
        self.url = url


    ##USER

    def add_user(self, user):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO users (id, username, password, name, surname, email, img_url, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                data = [user.id, user.username, user.password, user.name, user.surname, user.email, user.img_url, False]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add user error: ", err)
        
        return user
        
    def get_user(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT id, username, password, name, surname, email, img_url, is_admin FROM users WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                user = User(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7])
                return user
        except Exception as err:
            print("Get user error: ", err)
        
        return None

    def get_username_by_id(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT username FROM users WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                username = cursor.fetchone()
                cursor.close()
                if not username:
                    return None
                return username
        except Exception as err:
            print("Get user error: ", err)
    
        return None

    def get_user_by_username(self,username):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM users WHERE username = %s"
                data = [username]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                user = User(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7])
                return user
        except Exception as err:
            print("Get user by username error: ", err)
        
        return None

    def get_all_users(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM users"
                cursor.execute(statement)
                users = cursor.fetchall()
                cursor.close()
                return users
        except Exception as err:
            print("Get all user error: ", err)
        
        return None

    def delete_user(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
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
            "is_admin": "is_admin",
        }

        try:
            with dbapi2.connect(self.url) as connection:
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

    def is_user_admin(self,user_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT is_admin FROM users WHERE id = %s"
                data = [user_id]
                cursor.execute(statement, data)
                value = cursor.fetchone()[0]
                cursor.close()
                return value                
        except Exception as err:
            print("Get user is_admin error: ", err)



    ##ROUTE

    def add_route(self, route):
        try:
            with dbapi2.connect(self.url) as connection:
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
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT id, user_id, name, description, img_url FROM routes WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                route = Route(value[0], value[1], value[2], value[3], value[4])
                return route
        except Exception as err:
            print("Get route error: ", err)

    def get_all_routes(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT id, user_id, name, description FROM routes"
                cursor.execute(statement)
                cities = cursor.fetchall()
                cursor.close()
                return cities
        except Exception as err:
            print("Get all route error: ", err)
        
        return None

    def get_routes_by_userid(self,user_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM routes WHERE user_id = %s"
                data = [user_id]
                cursor.execute(statement, data)
                routes = cursor.fetchall()
                cursor.close()
                return routes
        except Exception as err:
            print("Get routes by userid error: ", err)

    def get_routename_activityid_activity_name(self,route_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT routes.name, route_activities.activity_id, activities.name FROM routes INNER JOIN route_activities ON routes.id = route_activities.route_id INNER JOIN activities ON route_activities.activity_id = activities.id WHERE routes.id = %s"
                data = [route_id]
                cursor.execute(statement, data)
                routes = cursor.fetchall()
                cursor.close()
                return routes
        except Exception as err:
            print("Get route name activityid activity name error: ", err)

    def delete_route(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM routes WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Delete user error: ", err)

    def update_route(self, id, attributes, values):
        attributes_table = {
            "user_id": "user_id",
            "name": "name",
            "description": "description",
            "img_url": "img_url"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE routes SET "
                for i in range(len(attributes) - 1):
                    statement += attributes_table[attributes[i]] + " = %s ,"
                statement += attributes_table[attributes[-1]] + " = %s WHERE id = %s"
                values.append(id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update user error: ", err)


    ##ACTIVITY

    def get_activity(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT id, name, description FROM activities WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                activity = Activity(value[0], value[1], value[2])
                return activity
        except Exception as err:
            print("Get activity error: ", err)
        
        return None

    def get_activity_name_with_image(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT name FROM activities WHERE id = %s UNION SELECT image_url FROM activity_image WHERE activity_id = %s"
                data = [id, id]
                cursor.execute(statement, data)
                value = cursor.fetchall()
                cursor.close()
                if not value:
                    return None
                return value
        except Exception as err:
            print("Get activity with image error: ", err)
        
        return None

    def get_all_activities(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT id, name, description FROM activities"
                cursor.execute(statement)
                activities = cursor.fetchall()
                cursor.close()
                return activities
        except Exception as err:
            print("Get activity error: ", err)
        
        return None

    def add_activity(self,activity):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO activities (id, name, description) VALUES (%s, %s, %s)"
                data = [activity.id, activity.name, activity.description]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add route error: ", err)
        
        return activity

    def update_activity(self, id, attributes, values):
        attributes_table = {
            "name": "name",
            "description": "description",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE activities SET "
                for i in range(len(attributes) - 1):
                    statement += attributes_table[attributes[i]] + " = %s ,"
                statement += attributes_table[attributes[-1]] + " = %s WHERE id = %s"
                values.append(id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update user error: ", err)

    def delete_activity(self,id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM activities WHERE id = %s"
                data = [id]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Delete user error: ", err)


    ##route_Activities

    def get_route_activities(self,route_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT activity_id FROM route_activities WHERE route_id = %s"
                data = [route_id]
                cursor.execute(statement, data)
                activity_ids = cursor.fetchall()
                activities = []
                for activity_id in activity_ids:
                    statement = "SELECT id, name, description, activity_image.image_url FROM activities INNER JOIN activity_image ON %s = activity_image.activity_id AND id = %s"
                    data = [activity_id, activity_id]
                    cursor.execute(statement, data)
                    activities.append(cursor.fetchone())

                cursor.close()
                return activities
        except Exception as err:
            print("Get route error: ", err)

    def add_activity_to_route(self, activity_id, route_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO route_activities (activity_id, route_id) VALUES (%s, %s)"
                data = [activity_id, route_id]
                cursor.execute(statement, data)
                cursor.close()

                return activity_id
        except Exception as err:
            print("Get route error: ", err)

    def update_route_activity(self, id, attributes, values):
        attributes_table = {
            "activity_id": "activity_id",
            "route_id": "route_id",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE route_activities SET "
                for i in range(len(attributes) - 1):
                    statement += attributes_table[attributes[i]] + " = %s ,"
                statement += attributes_table[attributes[-1]] + " = %s WHERE id = %s"
                values.append(id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update route activity error: ", err)


    def delete_route_activity(self,route_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM route_activities WHERE id = %s"
                data = [route_id]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Delete route_activities error: ", err)


    ##route_Score

    def rate_route(self, route_id, user_id, score):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO route_score (user_id, route_id, score) VALUES (%s, %s, %s)"
                data = [user_id, route_id, score]
                cursor.execute(statement, data)
                cursor.close()

        except Exception as err:
            print("Rate route error: ", err)

    def check_user_rated_route(self, route_id, user_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM route_score WHERE user_id = %s AND route_id = %s"
                data = [user_id, route_id]
                cursor.execute(statement, data)
                if not cursor.fetchall():
                    return False
                cursor.close()
                return True

        except Exception as err:
            print("Rate route error: ", err)

    def get_route_score(self, route_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (CAST(SUM(score) AS DECIMAL)/COUNT(route_id = %s)) AS total FROM route_score WHERE route_id = %s GROUP BY route_id"
                data = [route_id, route_id]
                cursor.execute(statement, data)
                score = cursor.fetchone()[0]
                score = round(score, 2)
                cursor.close()
                return score

        except Exception as err:
            print("Get route score error: ", err)

    def update_route_score(self, id, attributes, values):
        attributes_table = {
            "user_id": "user_id",
            "route_id": "route_id",
            "score": "score"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE route_activities SET "
                for i in range(len(attributes) - 1):
                    statement += attributes_table[attributes[i]] + " = %s ,"
                statement += attributes_table[attributes[-1]] + " = %s WHERE id = %s"
                values.append(id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update route activity error: ", err)


    def delete_route_score(self, user_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM route_score WHERE id = %s"
                data = [user_id]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Delete route_activities error: ", err)
