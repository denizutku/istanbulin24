import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
        """CREATE TABLE IF NOT EXISTS users 
    (
        user_id SERIAL NOT NULL PRIMARY KEY,
        user_name VARCHAR(15) UNIQUE NOT NULL,
        email VARCHAR (50) NOT NULL,
        password VARCHAR (50) NOT NULL,
        name VARCHAR (50) NOT NULL,
        surname VARCHAR (50) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        gender VARCHAR (1) NOT NULL,
        address VARCHAR (250) NOT NULL,
        last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        register_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE

    )""",
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