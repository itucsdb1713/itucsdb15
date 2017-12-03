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

class ContractDatabase:
    @classmethod
    def add_contract(cls, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, SignDate, EndDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            UserID = 1
            CreateUserID = 1
            query = """INSERT INTO ContractInfo (UserID, CreateUserID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, 
                                                              SignDate, EndDate, CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (UserID, CreateUserID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium,
                                                              SignDate, EndDate, CreateDate,))
            cursor.close()