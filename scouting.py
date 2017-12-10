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
    if current_user.userType == 'admin' or current_user.userType == "Scout":
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':
                query = """ SELECT x.ID, x.Name, x.Surname, x.Point, x.CreateDate, y.HomeTeamName, y.AwayTeamName, y.ArenaName, y.MatchDate  FROM ObservedPlayerInfo as x JOIN FixtureInfo as y ON x.MatchId = y.Id ORDER BY x.CreateDate DESC"""
                cursor.execute(query)
                observedPlayers = cursor.fetchall()
                connection.commit()
                return render_template('scouting.html',observedPlayers=observedPlayers)

            else:
                deletes = request.form.getlist('scouting_to_delete')

                for delete in deletes:
                    query = "DELETE FROM ObservedPlayerInfo WHERE ID='%d'" % int(delete)
                    cursor.execute(query)

                return redirect(url_for('site.scouting_page'))
    else:
        return render_template('error.html')


@site.route('/scouting/add', methods=['GET', 'POST'])
@login_required
def scouting_add():
    if current_user.userType == 'admin' or current_user.userType == "Scout":
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
    else:
        return render_template('error.html')


@site.route('/scouting/update/<int:observedID>', methods=['GET', 'POST'])
@login_required
def scouting_update(observedID):
    if current_user.userType == 'admin' or current_user.userType == "Scout":
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':

                query = """ SELECT ID, Name, Surname, Point FROM ObservedPlayerInfo WHERE ID='%d'""" %(observedID)
                cursor.execute(query)
                observedPlayer = cursor.fetchone()
                query = """ SELECT * FROM FixtureInfo"""  # typeid 4 for training
                cursor.execute(query)
                fixture_data = cursor.fetchall()
                connection.commit()

                return render_template('scouting_update.html', observedPlayer=observedPlayer,fixture_data=fixture_data)
            else:

                new_Match = request.form['matchType']
                new_Name = request.form['observedName']
                new_Surname = request.form['observedSurname']
                new_Point = request.form['observedPoint']
                new_Date = datetime.datetime.now()

                query = """SELECT * FROM ObservedPlayerInfo WHERE ID = %d""" % (observedID)
                cursor.execute(query)
                observedPlayerInfo = cursor.fetchone()
                observedPlayer = list(observedPlayerInfo)

                if new_Name != "":
                    observedPlayer[5] = new_Name
                if new_Surname != "":
                    observedPlayer[6] = new_Surname
                if new_Point != "":
                    observedPlayer[3] = new_Point


                query = """UPDATE ObservedPlayerInfo 
                                                    SET Name = '%s', Surname= '%s', Point= '%s', MatchID= '%d', CreateDate= '%s'
                                                    WHERE ID = %d """ % (
                    observedPlayer[5], observedPlayer[6], observedPlayer[3], int(new_Match),new_Date, observedID)
                cursor.execute(query)
                cursor.close()

                connection.commit()

                return redirect(url_for('site.scouting_page'))
    else:
        return render_template('error.html')




