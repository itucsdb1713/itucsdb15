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


@site.route('/scouting', methods=['GET', 'POST'])
@login_required
def scouting_page():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()

        if request.method == 'GET':
            query = """ SELECT x.ID, x.Name, x.Surname, x.Point, x.CreateDate, y.HomeTeamName, y.AwayTeamName, y.ArenaName, y.MatchDate  FROM ObservedPlayerInfo as x JOIN FixtureInfo as y ON x.MatchId = y.Id ORDER BY x.CreateDate DESC"""
            cursor.execute(query)
            observedPlayers = cursor.fetchall()
            connection.commit()
            return render_template('scouting.html',observedPlayers=observedPlayers)


@site.route('/scouting/add', methods=['GET', 'POST'])
@login_required
def scouting_add():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()

        if request.method == 'GET':
            query = """ SELECT * FROM FixtureInfo"""
            cursor.execute(query)
            match_data = cursor.fetchall()
            return render_template('scouting_add.html', match_data=match_data)

        else:
            matchType = request.form['matchType']
            observedName = request.form['observedName']
            observedSurname = request.form['observedSurname']
            observedPoint = request.form['observedPoint']
            if observedPoint == '':
                observedPoint = 0
            query = "INSERT INTO ObservedPlayerInfo(MatchID, ScoutID, Name, Surname, Point,CreateDate) VALUES('%d', '%d', '%s', '%s','%d','%s')" % (int(matchType), current_user.id, observedName, observedSurname, int(observedPoint), datetime.datetime.now())
            cursor.execute(query)

            connection.commit()

            return redirect(url_for('site.scouting_page'))




