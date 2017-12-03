import psycopg2 as dbapi2
from database import database
import datetime

class PremiumDatabase:
    @classmethod
    def add_premium(cls, UserID, TypeID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            CreateUserID = 1
            query = """INSERT INTO PremiumInfo (UserID, TypeID, CreateUserID, CreateDate) VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (UserID, TypeID, CreateUserID, CreateDate,))
            cursor.close()

