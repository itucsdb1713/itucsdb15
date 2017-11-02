import psycopg2 as dbapi2
import json
import re
import os
from passlib.apps import custom_app_context as pwd_context
import datetime

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

            ################ Mehmet Taha Çorbacıoğlu ################
            query = """DROP TABLE IF EXISTS PositionParameter CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE PositionParameter (
                                        ID SERIAL PRIMARY KEY,
                                        PositionName VARCHAR(50) UNIQUE NOT NULL
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS UserTypeParameter CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE UserTypeParameter (
                                        ID SERIAL PRIMARY KEY,
                                        TypeName VARCHAR(50) UNIQUE NOT NULL
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS CityParameter CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE CityParameter (
                                        ID SERIAL PRIMARY KEY,
                                        CityName VARCHAR(50) UNIQUE NOT NULL
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS UserInfo CASCADE"""
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
                                        Surname VARCHAR (50),
                                        FOREIGN KEY (TypeID) REFERENCES UserTypeParameter(ID),
                                        FOREIGN KEY (PositionID) REFERENCES PositionParameter(ID),
                                        FOREIGN KEY (BirthCityID) REFERENCES CityParameter(ID),
                                        FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                        )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS LogInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE LogInfo (
                                      UserID SERIAL PRIMARY KEY,
                                      Username varchar(50) UNIQUE NOT NULL,
                                      Password varchar(50) NOT NULL,
                                      LastLoginDate TIMESTAMP,
                                      FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)
                                    )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS InjuryInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE InjuryInfo (
                                      ID SERIAL PRIMARY KEY,
                                      UserID INTEGER NOT NULL,
                                      RecoveryTime INTEGER NOT NULL,
                                      CreateUserID INTEGER NOT NULL,
                                      CreateDate TIMESTAMP NOT NULL,
                                      Injury VARCHAR(500) NOT NULL,
                                      InjuryArea VARCHAR(50) NOT NULL,
                                      FOREIGN KEY (UserID) REFERENCES UserInfo(UserID),
                                      FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                    )"""
            cursor.execute(query)

            ################ ufuk sahar ####################


            # TrainingTypeParameter table is deleted #
            query = """DROP TABLE IF EXISTS TrainingTypeParameter CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE TrainingTypeParameter (
                                                          ID SERIAL PRIMARY KEY,
                                                          TrainingTypeName VARCHAR(50) NOT NULL
                                                                        )"""
            cursor.execute(query)
            # TrainingTypeParameter table is created #


            # TrainingInfo table is deleted #
            query = """DROP TABLE IF EXISTS TrainingInfo CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE TrainingInfo (
                                                  ID SERIAL PRIMARY KEY,
                                                  TypeID INTEGER NOT NULL,
                                                  CreateUserID INTEGER NOT NULL,
                                                  TrainingDate TIMESTAMP NOT NULL,
                                                  CreateDate DATE NOT NULL,
                                                  TrainingName VARCHAR(50) NOT NULL,
                                                  Location VARCHAR(500) NOT NULL,
                                                  FOREIGN KEY (TypeID) REFERENCES TrainingTypeParameter (ID),
                                                  FOREIGN KEY (CreateUserID) REFERENCES UserInfo (UserID)
                                                            )"""
            cursor.execute(query)
            # TrainingInfo table is created #


            # TrainingMapInfo table is deleted #
            query = """DROP TABLE IF EXISTS TrainingMapInfo CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE TrainingMapInfo (
                                                     ID SERIAL PRIMARY KEY,
                                                     TrainingID INTEGER NOT NULL,
                                                     UserID INTEGER NOT NULL,
                                                     IsAttend BIT NOT NULL,
                                                     Excuse VARCHAR(250) NOT NULL, 
                                                     FOREIGN KEY (TrainingID) REFERENCES TrainingInfo (ID),
                                                     FOREIGN KEY (UserID) REFERENCES UserInfo (UserID)

                                                                  )"""
            cursor.execute(query)
            # TrainingMapInfo table is created #

            ################ Utku Anıl Saykara ####################

            query = """DROP TABLE IF EXISTS ContractInfo CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE ContractInfo (
                                                ID SERIAL PRIMARY KEY,
                                                UserID INTEGER NOT NULL,
                                                CreateUserID INTEGER NOT NULL,
                                                Salary MONEY DEFAULT 0,
                                                SignPremium MONEY DEFAULT 0,
                                                MatchPremium MONEY DEFAULT 0,
                                                GoalPremium MONEY DEFAULT 0,
                                                AssistPremium MONEY DEFAULT 0,
                                                SignDate TIMESTAMP NOT NULL,
                                                EndDate TIMESTAMP NOT NULL,
                                                CreateDate TIMESTAMP NOT NULL,
                                                FOREIGN KEY (UserID) REFERENCES UserInfo(UserID),
                                                FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                                )"""

            cursor.execute(query)
            # ContractInfo table is created #

            connection.commit()
            cursor.close()


database = DatabaseOPS()
