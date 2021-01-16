from flask import current_app
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, name, surname, email):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.active = True
        self.is_admin = False

        @property
        def get_id(self):
            return self.id

        @property
        def is_active(self):
            return self.active

