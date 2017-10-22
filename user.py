from flask_login import UserMixin
import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class UserDatabase:
    @classmethod
    def add_user(cls, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO USERS (USERNAME, PASSWORD) VALUES (
                                                  %s,
                                                  %s
                                )"""
            hashp = pwd_context.encrypt(password)
            try:
                cursor.execute(query, (username, hashp,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM USERS WHERE USERNAME=%s"""

            user_data = None

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2])
            else:
                return -1

    @classmethod
    def select_user_with_id(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM USERS WHERE USER_ID=%s"""

            try:
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2])
            else:
                return -1