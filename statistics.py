from handlers import site
from database import database
from user import *
import psycopg2 as dbapi2
import datetime
from passlib.apps import custom_app_context as pwd_context
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user, current_user, login_required, logout_user
import urllib

class StatisticsDatabase:
    @classmethod
    def add_statistics(cls, ID, Goal, Asist, Match):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM StatisticsInfo WHERE ID = %s""" % (ID)
            cursor.execute(query)
            statisticsInfo = cursor.fetchone()
            statistics = list(statisticsInfo)
            if Goal != "":
                statistics[1] = int(Goal) + int(statistics[1])
            if Asist != "":
                statistics[2] = int(Asist) + int(statistics[2])
            if Match != "":
                statistics[3] = int(Match) + int(statistics[3])

            query = """UPDATE StatisticsInfo 
                            SET Goal = '%s', Assist= '%s', Match= '%s'
                            WHERE ID = '%s' """ % (str(statistics[1]), str(statistics[2]), str(statistics[3]), str(ID))
            cursor.execute(query)
            cursor.close()

    @classmethod
    def update_statistics(cls, ID, Goal, Assist, Match):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM StatisticsInfo WHERE ID = %d""" % (ID)
            cursor.execute(query)
            statisticsInfo = cursor.fetchone()
            statistics = list(statisticsInfo)
            if Goal != "":
                statistics[1] = Goal
            if Assist != "":
                statistics[2] = Assist
            if Match != "":
                statistics[3] = Match

            query = """UPDATE StatisticsInfo 
                                SET Goal = '%s', Assist= '%s', Match= '%s'
                                WHERE ID = %d """ % (statistics[1], statistics[2], statistics[3], ID)
            cursor.execute(query)
            cursor.close()

    @classmethod
    def DeleteStatistic(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """UPDATE StatisticsInfo 
                                            SET Goal = %d, Assist= %d, Match= %d
                                            WHERE ID = '%s' """ % (0, 0, 0, ID)
            cursor.execute(query)
            cursor.close()

    @classmethod
    def GetAllStatistics(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT k.ID, l.name, l.surname, k.Goal, k.Assist, k.Match FROM StatisticsInfo as k,UserInfo as l, Parameters as m 
                        WHERE k.ID = l.UserID and l.UserTypeID = m.ID and m.name = 'Footballer' """
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                statistics = cursor.fetchall()
                connection.commit()
            cursor.close()
            return statistics

    @classmethod
    def GetStatistic(cls,ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT k.ID, l.name, l.surname, k.Goal, k.Assist, k.Match FROM StatisticsInfo as k,UserInfo as l
                             WHERE k.ID = l.UserID and k.ID = %d"""%(ID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                statistic = cursor.fetchone()
                connection.commit()
            cursor.close()
            return statistic

    @classmethod
    def getStatisticUsers(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT k.UserID, k.Name, k.Surname FROM UserInfo as k, parameters as l WHERE k.UserTypeID = l.ID and l.name ='Footballer'  """

            try:
                cursor.execute(query)
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return user_data