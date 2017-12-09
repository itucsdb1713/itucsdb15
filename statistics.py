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
            query = """SELECT * FROM StatisticsInfo WHERE ID = %d""" % (ID)
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
                            SET Goal = '%s', Asist= '%s', Match= '%s'
                            WHERE ID = %d """ % (statistics[1], statistics[2], statistics[3], ID)
            cursor.execute(query)
            cursor.close()

    @classmethod
    def update_statistics(cls, ID, Goal, Asist, Match):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM StatisticsInfo WHERE ID = %d""" % (ID)
            cursor.execute(query)
            statisticsInfo = cursor.fetchone()
            statistics = list(statisticsInfo)
            if Goal != "":
                statistics[1] = Goal
            if Asist != "":
                statistics[2] = Asist
            if Match != "":
                statistics[3] = Match

            query = """UPDATE StatisticsInfo 
                                SET Goal = '%s', Asist= '%s', Match= '%s'
                                WHERE ID = %d """ % (statistics[1], statistics[2], statistics[3], ID)
            cursor.execute(query)
            cursor.close()

    @classmethod
    def DeleteStatistic(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """UPDATE StatisticsInfo 
                                            SET Goal = %d, Asist= %d, Match= %d
                                            WHERE ID = %d """ % (0, 0, 0, ID)
            cursor.execute(query)
            cursor.close()