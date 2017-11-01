import psycopg2 as dbapi2
import json
import re
import os
from passlib.apps import custom_app_context as pwd_context

class DatabaseOPS:
    def __init__(self):

        VCAP_SERVICES = os.getenv('VCAP_SERVICES')

        if VCAP_SERVICES is not None:
            self.config = DatabaseOPS.get_elephantsql_dsn(VCAP_SERVICES)
        else:
            self.config = """user='postgres' password='12345'
                            host='localhost' port=5432 dbname='beeINfootball'"""

    @classmethod
    def get_elephantsql_dsn(cls, vcap_services):
        """Returns the data source name for ElephantSQL."""
        parsed = json.loads(vcap_services)
        uri = parsed["elephantsql"][0]["credentials"]["uri"]
        match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
        user, password, host, _, port, dbname = match.groups()
        dsn = """user='{}' password='{}' host='{}' port={}
                 dbname='{}'""".format(user, password, host, port, dbname)
        return dsn

    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # Mehmet Taha Çorbacıoğlu
            query = """DROP TABLE IF EXISTS PositionParameter"""
            cursor.execute(query)
            query = """CREATE TABLE PositionParameter (
                                        ID SERIAL PRIMARY KEY,
                                        PositionName VARCHAR(50) UNIQUE NOT NULL
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS UserTypeParameter"""
            cursor.execute(query)
            query = """CREATE TABLE UserTypeParameter (
                                        ID SERIAL PRIMARY KEY,
                                        TypeName VARCHAR(50) UNIQUE NOT NULL
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS CityParameter"""
            cursor.execute(query)
            query = """CREATE TABLE CityParameter (
                                        ID SERIAL PRIMARY KEY,
                                        CityName VARCHAR(50) UNIQUE NOT NULL
                                        )"""

            query = """DROP TABLE IF EXISTS UserInfo"""
            cursor.execute(query)
            query = """CREATE TABLE UserInfo (
                                        UserID SERIAL PRIMARY KEY,
                                        TypeID INTEGER NOT NULL,
                                        PositionID INTEGER,
                                        BirthCityID INTEGER,
                                        CreateUserID INTEGER NOT NULL,
                                        No INTEGER,
                                        Birthday DATE,
                                        CreateDate TIMESTAMP NOT NULL,
                                        Name VARCHAR(50),
                                        Surname VARCHAR (50)
                                        FOREIGN KEY TypeID REFERENCES UserTypeParameter(ID)
                                        FOREIGN KEY PositionID REFERENCES PositionParameter(ID)
                                        FOREIGN KEY BirthCityID REFERENCES CityParameter(ID)
                                        FOREIGN KEY CreateUserID REFERENCES UserInfo(UserID)
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS LogInfo"""
            cursor.execute(query)
            query = """CREATE TABLE LogInfo (
                                      UserID SERIAL PRIMARY KEY,
                                      Username varchar(50) UNIQUE NOT NULL,
                                      Password varchar(50) NOT NULL,
                                      LastLoginDate TIMESTAMP
                                      FOREIGN KEY UserID REFERENCES UserInfo(UserID)
                                    )"""
            cursor.execute(query)

            hashp = pwd_context.encrypt('12345')
            query = """INSERT INTO LogInfo(Username, Password) VALUES ('admin', %s)"""
            cursor.execute(query, (hashp,))

            connection.commit()
            cursor.close()

database = DatabaseOPS()