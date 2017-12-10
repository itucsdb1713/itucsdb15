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
    def add_injury(cls,UserID, RecoveryTime, Injury, InjuryArea):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            CreateUserID = current_user.id
            query = """INSERT INTO InjuryInfo (UserID, RecoveryTime, CreateUserID, CreateDate, Injury, InjuryArea) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (UserID, RecoveryTime, CreateUserID, CreateDate, Injury, InjuryArea,))
            cursor.close()

    @classmethod
    def GetInjuryInfo(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT k.ID, l.name,l.surname, k.RecoveryTime, k.Injury, k.InjuryArea, k.CreateDate 
                        FROM InjuryInfo as k, UserInfo as l WHERE k.UserID = l.UserID and k.ID = %d """%(ID)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                injuryInfo = cursor.fetchone()
                connection.commit()

            cursor.close()
            return injuryInfo

    @classmethod
    def GetInjuryInfoUser(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT k.RecoveryTime, k.Injury, k.InjuryArea, k.CreateDate 
                            FROM InjuryInfo as k, UserInfo as l WHERE k.UserID = l.UserID and l.UserID = %d """ % (ID)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                injuryInfo = cursor.fetchone()
                connection.commit()

            cursor.close()
            return injuryInfo

    def GetCurrentInjuryDays(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            now = datetime.datetime.now()
            query = """SELECT TOP 1 * FROM LogInfo WHERE UserID=%s and (now - CreateDate).DAY < RecoveryTime """

            try:
                cursor.execute(query, (userID,))
                injuryInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if injuryInfo:
                Injury(ID=injuryInfo[0], userID=injuryInfo[1], recoveryTime=injuryInfo[2], createUserID=injuryInfo[3],
                              createDate=injuryInfo[4], injury=injuryInfo[5], injuryArea=injuryInfo[6],)
                return Injury.recoveryTime - (now - Injury.createDate).days
            else:
                return 0

    @classmethod
    def GetInjuries(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT k.ID, l.name, l.surname, k.recoveryTime, k.injury, k.injuryArea, k.createDate
                        FROM InjuryInfo as k, UserInfo as l WHERE k.UserID = l.UserID"""
            try:
                cursor.execute(query)
                injuryInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return injuryInfo

    @classmethod
    def DeleteInjury(cls,ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM InjuryInfo WHERE ID = %s"""%(ID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_injury(cls, ID, RecoveryTime, Injury, InjuryArea):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM InjuryInfo WHERE ID = %d""" % (ID)
            cursor.execute(query)
            injuryInfo = cursor.fetchone()
            injury = list(injuryInfo)
            if RecoveryTime != "":
                injury[2] = RecoveryTime
            if Injury != "":
                injury[5] = Injury
            if InjuryArea != "":
                injury[6] = InjuryArea

            query = """UPDATE InjuryInfo 
                            SET RecoveryTime = '%s', Injury= '%s', InjuryArea= '%s'
                            WHERE ID = %d """ % (injury[2], injury[5], injury[6], ID)
            cursor.execute(query)
            cursor.close()

