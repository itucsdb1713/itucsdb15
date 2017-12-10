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


@site.route('/fixture', methods=['GET', 'POST'])
@login_required
def fixture_page():
    if current_user.userType == 'admin':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':
                query = """ SELECT x.ID, x.HomeTeamName, x.AwayTeamName, x.ArenaName, y.Name, x.HomeTeamScore, x.AwayTeamScore, x.Matchdate FROM FixtureInfo As x JOIN Parameters as y ON x.CityId = y.Id ORDER BY x.MatchDate DESC"""
                cursor.execute(query)
                fixture = cursor.fetchall()
                connection.commit()
                return render_template('fixture.html', fixture=fixture)
            else:
                deletes = request.form.getlist('fixture_to_delete')

                for delete in deletes:
                    query = "DELETE FROM FixtureInfo WHERE ID='%d'" % int(delete)
                    cursor.execute(query)
                return redirect(url_for('site.fixture_page'))
    else:
        return render_template('error.html')


@site.route('/fixture/add', methods=['GET', 'POST'])
@login_required
def fixture_add():
    if current_user.userType == 'admin':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':
                query = """ SELECT * FROM PARAMETERS WHERE TYPEID=3"""  # typeid 3 for city
                cursor.execute(query)
                city_data = cursor.fetchall()
                return render_template('fixture_add.html', city_data=city_data)
            else:
                fixtureHomeName = request.form['fixtureHomeName']
                fixtureAwayName = request.form['fixtureAwayName']
                fixtureArena = request.form['fixtureArena']
                fixtureCity = request.form['fixtureCity']
                matchDate = request.form['matchDate']


                query = "INSERT INTO FixtureInfo(CityID,HomeTeamName,AwayTeamName,ArenaName,matchDate) VALUES('%d', '%s', '%s', '%s','%s')" % (
                int(fixtureCity), fixtureHomeName, fixtureAwayName, fixtureArena, matchDate)
                cursor.execute(query)

                connection.commit()

                return redirect(url_for('site.fixture_page'))
    else:
        return render_template('error.html')

@site.route('/fixture/update/<int:matchID>', methods=['GET', 'POST'])
@login_required
def fixture_update(matchID):
    if current_user.userType == 'admin':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':

                query = """ SELECT x.ID, x.HomeTeamName, x.AwayTeamName, x.ArenaName, x.matchDate, x.HomeTeamScore, x.AwayTeamScore FROM FixtureInfo As x JOIN Parameters as y ON x.CityId = y.Id WHERE x.ID=%d""" %(matchID)
                cursor.execute(query)
                match = cursor.fetchone()
                query = """ SELECT * FROM PARAMETERS WHERE TYPEID=3"""  # typeid 3 for city
                cursor.execute(query)
                city_data = cursor.fetchall()
                connection.commit()

                return render_template('fixture_update.html', match=match, city_data=city_data)
            else:

                new_Home = request.form['fixtureHomeName']
                new_Away = request.form['fixtureAwayName']
                new_Arena = request.form['fixtureArena']
                new_HomeScore = request.form['fixtureHomeScore']
                new_AwayScore = request.form['fixtureAwayScore']
                new_City = request.form['fixtureCity']
                new_Date = request.form['matchDate']

                query = """SELECT * FROM FixtureInfo WHERE ID = %d""" % (matchID)
                cursor.execute(query)
                fixtureInfo = cursor.fetchone()
                fixture = list(fixtureInfo)
                if new_Home != "":
                    fixture[5] = new_Home
                if new_Away != "":
                    fixture[6] = new_Away
                if new_Arena != "":
                    fixture[7] = new_Arena
                if new_HomeScore != "":
                    fixture[2] = new_HomeScore
                if new_AwayScore != "":
                    fixture[3] = new_AwayScore
                if new_City != "":
                    fixture[1] = new_City
                if new_Date != "":
                    fixture[4] = new_Date

                query = """UPDATE FixtureInfo 
                                        SET HomeTeamName = '%s', AwayTeamName= '%s', ArenaName= '%s', CityID= '%d', HomeTeamScore= '%s', AwayTeamScore= '%s', MatchDate= '%s'
                                        WHERE ID = %d """ % (
                    fixture[5], fixture[6], fixture[7], int(fixture[1]), fixture[2], fixture[3], fixture[4], matchID)
                cursor.execute(query)
                cursor.close()


                connection.commit()
                return redirect(url_for('site.fixture_page'))
    else:
        return render_template('error.html')
