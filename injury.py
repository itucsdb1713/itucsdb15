from flask_login import UserMixin
import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user

class User(UserMixin):
    def __init__(self, id, username, password, lastLoginDate):
        self.id = id
        self.username = username
        self.password = password
        self.lastLoginDate = lastLoginDate

class InjuryDatabase:
    @classmethod
    def add_injury(cls, RecoveryTime, Injury, InjuryArea):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            UserID = 1
            CreateUserID = 1
            query = """INSERT INTO InjuryInfo (UserID, RecoveryTime, CreateUserID, CreateDate, Injury, InjuryArea) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (UserID, RecoveryTime, CreateUserID, CreateDate, Injury, InjuryArea,))
            cursor.close()