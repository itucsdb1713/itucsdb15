from flask_login import UserMixin
import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user

class User(UserMixin):
    def __init__(self, id, username, password, lastLoginDate, userType):
        self.id = id
        self.username = username
        self.password = password
        self.lastLoginDate = lastLoginDate
        self.userType = userType

class UserDatabase:
    @classmethod
    def add_user(cls, TypeID, PositionID, BirthCityID, No, Birthday, Name, Surname, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO UserInfo (UserTypeID, PositionID, CityID, CreateUserID, No, Birthday, 
                                                              CreateDate, Name, Surname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(TypeID), str(PositionID), str(BirthCityID), str(current_user.id), str(No), Birthday, datetime.datetime.now(), Name, Surname))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            
            query = """SELECT MAX(UserID) FROM UserInfo """
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                userID = cursor.fetchone()
                connection.commit()
            hashp = pwd_context.encrypt(password)
            query = """INSERT INTO LogInfo (userID, Username, Password) VALUES ('%d','%s','%s')"""%(userID[0], username, hashp)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            query = """SELECT name FROM Parameters WHERE ID = '%s' """%(TypeID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                parameterName = cursor.fetchone()
                connection.commit()
                
            if parameterName[0] == 'Footballer':
                query = """INSERT INTO StatisticsInfo (ID) VALUES ('%s')"""%(str(userID[0]))
                try:
                    cursor.execute(query)
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

            cursor.close()

    @classmethod
    def select_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM LogInfo WHERE Username=%s"""

            user_data = None

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            print(user_data)
            query = "SELECT y.Name FROM userinfo as x JOIN Parameters as y ON (x.usertypeid=y.id) WHERE x.userID='%d'" %(user_data[0])
            cursor.execute(query)
            user_type = cursor.fetchone()
            connection.commit()
            cursor.close()
            print("Select user with username: ",user_type[0])
            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2], lastLoginDate = user_data[3],userType = user_type[0])
            else:
                return -1

    @classmethod
    def select_user_with_id(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM LogInfo WHERE UserID=%s"""

            try:
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            query = "SELECT y.Name FROM userinfo as x JOIN Parameters as y ON (x.usertypeid=y.id) WHERE x.userID='%d'" % (
            user_data[0])

            cursor.execute(query)
            user_type = cursor.fetchone()
            connection.commit()
            cursor.close()
            print("Select user with id: ", user_type[0])
            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2], lastLoginDate = user_data[3], userType=user_type[0])
            else:
                return -1

    @classmethod
    def setLastLoginDate(cls, user):
        user.lastLoginDate = datetime.datetime.now()
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE LogInfo SET LastLoginDate =%s WHERE (UserID = %s)"""
            cursor.execute(query, (datetime.datetime.now(), user.id,))
            connection.commit()
            cursor.close()

    @classmethod
    def getUserContractAdd(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT UserID, Name, Surname FROM UserInfo WHERE UserInfo.UserID NOT IN(SELECT ContractInfo.UserID FROM ContractInfo) """

            try:
                cursor.execute(query)
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return user_data
    @classmethod
    def updateUser(cls, currentId, newName, newSurname, newType, newNo, newBirthday, newPosition, newCity):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            try:
                if(newName != ''):
                    query = "UPDATE USERINFO SET name='%s' WHERE userid = '%d'" % (newName, int(currentId))
                    cursor.execute(query)
                if(newSurname != ''):
                    query = "UPDATE USERINFO SET surname='%s' WHERE userid = '%d'" % (newSurname, int(currentId))
                    cursor.execute(query)
                if(newType != ''):
                    query = "UPDATE USERINFO SET usertypeid='%d' WHERE userid = '%d'" % (int(newType), int(currentId))
                    cursor.execute(query)
                if(newNo != ''):
                    query = "UPDATE USERINFO SET no='%d' WHERE userid = '%d'" % (int(newNo), int(currentId))
                    cursor.execute(query)
                if(newBirthday != ''):
                    query = "UPDATE USERINFO SET birthday='%s' WHERE userid = '%d'" % (newBirthday, int(currentId))
                    cursor.execute(query)
                if(newPosition != ''):
                    query = "UPDATE USERINFO SET positionid='%d' WHERE userid = '%d'" % (int(newPosition), int(currentId))
                    cursor.execute(query)
                if(newCity !=''):
                    query = "UPDATE USERINFO SET cityid='%d' WHERE userid = '%d'" % (int(newCity), int(currentId))
                    cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def deleteUser(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            try:
                query = "DELETE FROM USERINFO WHERE USERID = '%d' " % int(ID)
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()