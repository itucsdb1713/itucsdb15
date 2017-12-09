import psycopg2 as dbapi2
import json
import re
import os
from passlib.apps import custom_app_context as pwd_context
import datetime
import cities
city_Dict= dict()
city_Dict = cities.city_dict
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

            ################ ufuk sahar ####################

            query = """DROP TABLE IF EXISTS ParameterType CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE ParameterType (
                                                 ID SERIAL PRIMARY KEY,
                                                 Name VARCHAR(50) NOT NULL
                                                                )"""
            cursor.execute(query)


            query = """DROP TABLE IF EXISTS Parameters CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE Parameters (
                                                    ID SERIAL PRIMARY KEY,
                                                    TypeID INTEGER NOT NULL,
                                                    Name VARCHAR(50) NOT NULL,
                                                    FOREIGN KEY (TypeID) REFERENCES ParameterType(ID)
                                                    
                                                    )"""
            cursor.execute(query)



            ################ ufuk sahar ####################

            ################ Mehmet Taha Çorbacıoğlu ################


            query = """DROP TABLE IF EXISTS UserInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE UserInfo (
                                        UserID SERIAL PRIMARY KEY,
                                        UserTypeID INTEGER NOT NULL,
                                        PositionID INTEGER,
                                        CityID INTEGER,
                                        CreateUserID INTEGER NOT NULL,
                                        No INTEGER,
                                        Birthday DATE,
                                        CreateDate TIMESTAMP NOT NULL,
                                        Name VARCHAR(50),
                                        Surname VARCHAR (50),
                                        FOREIGN KEY (UserTypeID) REFERENCES Parameters(ID),
                                        FOREIGN KEY (PositionID) REFERENCES Parameters(ID),
                                        FOREIGN KEY (CityID) REFERENCES Parameters(ID),
                                        FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                        )"""
            cursor.execute(query)

            # StatisticsInfo table is deleted #
            query = """DROP TABLE IF EXISTS StatisticsInfo CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE StatisticsInfo (
                                                                ID INT PRIMARY KEY,
                                                                Goal INTEGER DEFAULT 0,
                                                                Assist INTEGER DEFAULT 0,
                                                                Match INTEGER DEFAULT 0,
                                                                FOREIGN KEY(ID) REFERENCES UserInfo(UserID)
                                                                )"""
            cursor.execute(query)
            # StatisticsInfo table is created #

            query = """DROP TABLE IF EXISTS LogInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE LogInfo (
                                      UserID INT PRIMARY KEY,
                                      Username varchar(50) UNIQUE NOT NULL,
                                      Password varchar(500) NOT NULL,
                                      LastLoginDate TIMESTAMP,
                                      FOREIGN KEY(UserID) REFERENCES UserInfo(UserID)
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
                                                  FOREIGN KEY (TypeID) REFERENCES Parameters (ID),
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

            # FixtureInfo table is deleted #
            query = """DROP TABLE IF EXISTS FixtureInfo CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE FixtureInfo (
                                                 ID SERIAL PRIMARY KEY,
                                                 CityID INTEGER NOT NULL,
                                                 HomeTeamScore INTEGER DEFAULT 0,
                                                 AwayTeamScore INTEGER DEFAULT 0,
                                                 MatchDate DATE,
                                                 HomeTeamName VARCHAR(100),
                                                 AwayTeamName VARCHAR(100),
                                                 ArenaName VARCHAR(100),
                                                 FOREIGN KEY (CityID) REFERENCES Parameters (ID)

                                                                                          )"""
            cursor.execute(query)
            # FixtureInfo table is created #

            # StadiumIncomeInfo table is deleted #
        #    query = """DROP TABLE IF EXISTS StadiumIncomeInfo CASCADE"""
        #    cursor.execute(query)

        #    query = """CREATE TABLE StadiumIncomeInfo (
        #                                               MatchID SERIAL PRIMARY KEY,
        #                                               AudienceIncome MONEY DEFAULT 0,
        #                                               StadiumExpense MONEY DEFAULT 0
        #                                                                                  )"""
        #    cursor.execute(query)
            # StadiumIncomeInfo table is created #
            ################ ufuk sahar ####################

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


            query = """DROP TABLE IF EXISTS PremiumInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE PremiumInfo (
                                                                ID SERIAL PRIMARY KEY,
                                                                UserID INTEGER NOT NULL,
                                                                PremiumTypeID INTEGER NOT NULL,
                                                                CreateUserID INTEGER NOT NULL,
                                                                CreateDate TIMESTAMP NOT NULL,
                                                                FOREIGN KEY (UserID) REFERENCES UserInfo(UserID),
                                                                FOREIGN KEY (PremiumTypeID) REFERENCES Parameters(ID),
                                                                FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)
                                                                )"""
            cursor.execute(query)
            # PremiumInfo table is created #

            query = """DROP TABLE IF EXISTS ObservedPlayerInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE ObservedPlayerInfo (
                                                                      ID SERIAL PRIMARY KEY,
                                                                      ScoutID INTEGER NOT NULL,
                                                                      MatchID INTEGER NOT NULL,
                                                                      Point INTEGER NOT NULL,
                                                                      CreateDate TIMESTAMP NOT NULL,
                                                                      Name VARCHAR(50),
                                                                      Surname VARCHAR (50),
                                                                      FOREIGN KEY (ScoutID) REFERENCES UserInfo(UserID),
                                                                      FOREIGN KEY (MatchID) REFERENCES FixtureInfo(ID)
                                                                      )"""
            cursor.execute(query)
            # ObservedPlayerInfo table is created #
            connection.commit()
            cursor.close()

    def adminInit(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            ################ Mehmet Taha Çorbacıoğlu ####################

            query = """INSERT INTO Parameters(Name,TypeID) VALUES ('admin',1)"""
            cursor.execute(query)

            query = """INSERT INTO UserInfo(UserTypeID, CreateUserID, CreateDate) VALUES (95, 1, %s)"""
            cursor.execute(query, (datetime.datetime.now(),))

            query = """SELECT MAX(UserID) FROM UserInfo """
            cursor.execute(query)
            userID = cursor.fetchone()

            hashp = pwd_context.encrypt('12345')
            query = """INSERT INTO LogInfo(UserID, Username, Password) VALUES (%s, 'admin', %s)"""
            cursor.execute(query, (userID[0],hashp,))

            connection.commit()
            cursor.close()
    def init_db(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            ### initialize the Parameter Types in ParameterType table. ###
            query = """INSERT INTO ParameterType(Name) VALUES ('User')"""
            cursor.execute(query)
            query = """INSERT INTO ParameterType(Name) VALUES ('Position')"""
            cursor.execute(query)
            query = """INSERT INTO ParameterType(Name) VALUES ('City')"""
            cursor.execute(query)
            query = """INSERT INTO ParameterType(Name) VALUES ('Training')"""
            cursor.execute(query)
            query = """INSERT INTO ParameterType(Name) VALUES ('Premium')"""
            cursor.execute(query)
            ##############################################################


            ### initialize the Parameters in Parameters table. ###
            # initialize the user parameters
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (1,'Trainer')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (1,'Footballer')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (1,'Doctor')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (1,'Scout')"""
            cursor.execute(query)

            # initialize the position parameters

            query = """INSERT INTO Parameters(TypeID, Name) VALUES (2,'Defence')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (2,'Striker')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (2,'GoalKeeper')"""
            cursor.execute(query)

            # initialize city parameters
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (3, %(city)s)"""
            cursor.executemany(query, city_Dict)

            # initialize training parameters
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (4,'Attack')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (4,'Defence')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (4,'Physical')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (4,'Mental')"""
            cursor.execute(query)

            # initialize premium parameters
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (5,'Goal Premium')"""
            cursor.execute(query)
            query = """INSERT INTO Parameters(TypeID, Name) VALUES (5,'Assist Premium')"""
            cursor.execute(query)
            ##############################################################
            connection.commit()
            cursor.close()


database = DatabaseOPS()
