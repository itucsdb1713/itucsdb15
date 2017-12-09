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
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()
        if request.method == 'GET':
            print("Fixture")
            if request.method == 'GET':
                query = """ SELECT x.ID, x.HomeTeamName, x.AwayTeamName, x.ArenaName, y.Name, x.HomeTeamScore, x.AwayTeamScore, x.Matchdate FROM FixtureInfo As x JOIN Parameters as y ON x.CityId = y.Id ORDER BY x.MatchDate DESC"""
                cursor.execute(query)
                fixture = cursor.fetchall()
                connection.commit()
            return render_template('fixture.html', fixture=fixture)


@site.route('/fixture/add', methods=['GET', 'POST'])
@login_required
def fixture_add():
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
