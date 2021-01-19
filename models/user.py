from flask import current_app
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, name, surname, email, img_url, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.img_url = img_url
        self.is_admin = is_admin
        self.active = True

        @property
        def get_id(self):
            return self.id

        @property
        def is_active(self):
            return self.active


