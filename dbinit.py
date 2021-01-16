import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """DROP TABLE IF EXISTS users cascade""",
    """DROP TABLE IF EXISTS routes cascade""",
    """DROP TABLE IF EXISTS activities cascade""",
    """DROP TABLE IF EXISTS route_activities cascade""",
    """DROP TABLE IF EXISTS route_score cascade""",

        """CREATE TABLE IF NOT EXISTS users 
    (
        id INT NOT NULL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR (255) NOT NULL,
        name VARCHAR (255) NOT NULL,
        surname VARCHAR (255) NOT NULL,
        email VARCHAR (255) NOT NULL

    )""",

    """CREATE TABLE IF NOT EXISTS routes
    (
        id INT NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        description VARCHAR (255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES userS(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS activities
    (
        id INT NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR (255) NOT NULL,
        img_url VARCHAR (255) NOT NULL

    )""",

    """CREATE TABLE IF NOT EXISTS route_activities
    (
        activity_id INT NOT NULL,
        route_id INT NOT NULL,
        FOREIGN KEY (activity_id) REFERENCES activities(id)ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (route_id) REFERENCES routes(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS route_score
    (
        user_id INT NOT NULL,
        route_id INT NOT NULL,
        score INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (route_id) REFERENCES routes(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",


    """INSERT INTO activities(id, name, description, img_url) VALUES (0, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (1, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (2, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (3, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (4, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (5, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (6, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (7, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (8, 'activity_name', 'activity_description', 'activity_imgurl')""",
    """INSERT INTO activities(id, name, description, img_url) VALUES (9, 'activity_name', 'activity_description', 'activity_imgurl')"""

]


def initialize():
    with dbapi2.connect(dbname="postgres",user="postgres",password="1",host="localhost") as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    # url = 
    # if url is None:
    #     print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
    #     sys.exit(1)
    initialize()