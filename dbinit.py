import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """DROP TABLE IF EXISTS users cascade""",
    """DROP TABLE IF EXISTS routes cascade""",
    """DROP TABLE IF EXISTS activities cascade""",

        """CREATE TABLE IF NOT EXISTS users 
    (
        id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR (255) NOT NULL,
        name VARCHAR (255) NOT NULL,
        surname VARCHAR (255) NOT NULL,
        email VARCHAR (255) NOT NULL

    )""",

    """CREATE TABLE IF NOT EXISTS routes
    (
        id SERIAL NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        description VARCHAR (255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES userS(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS activities
    (
        id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR (255) NOT NULL,
        img_url VARCHAR (255) NOT NULL

    )""",

    # """INSERT INTO routes(id, username, password, name, surname, email) VALUES
    # (
    #     0,
    #     'deniz',
    #     'deniz',
    #     'deniz',
    #     'deniz',
    #     'deniz'

    # )""",
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