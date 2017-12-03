import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user

class Injury():
    def __init__(self, ID, userID, recoveryTime, createUserID, createDate, injury, injuryArea):
        self.ID = ID
        self.userID = userID
        self.createUserID = createUserID
        self.recoveryTime = recoveryTime
        self.injury = injury
        self.injuryArea = injuryArea

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

    @classmethod
    def GetInjuryInfo(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM LogInfo WHERE UserID=%s """

            try:
                cursor.execute(query, (userID,))
                injuryInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if injuryInfo:
                return Injury(ID=injuryInfo[0], userID=injuryInfo[1], recoveryTime=injuryInfo[2], createUserID=injuryInfo[3],
                              createDate=injuryInfo[4], injury=injuryInfo[5], injuryArea=injuryInfo[6],)
            else:
                return -1