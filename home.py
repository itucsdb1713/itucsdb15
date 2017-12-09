from handlers import site
from database import database
from user import *
from contract import *
from injury import *

import datetime
import psycopg2 as dbapi2
from passlib.apps import custom_app_context as pwd_context
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user, current_user, login_required, logout_user
import urllib


@site.route('/')
@login_required
def home_page():
    now = datetime.datetime.now()

    return render_template('home.html', current_time=now.ctime(),user = current_user.username)

@site.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.login_page'))

@site.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = UserDatabase.select_user(request.form['username'])
        if user and user != -1:
            if pwd_context.verify(request.form['password'], user.password):
                UserDatabase.setLastLoginDate(user)
                login_user(user)
                print(current_user.username)
                return redirect(url_for('site.home_page'))


@site.route('/register', methods=['GET', 'POST'])
@login_required
def register_page():
    if request.method == 'GET':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=1"""  # typeid 1 for user type
            cursor.execute(query)
            userTypeData = cursor.fetchall()
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=2"""  # typeid 2 for position type
            cursor.execute(query)
            positionTypeData = cursor.fetchall()
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=3"""  # typeid 3 for city type
            cursor.execute(query)
            cityTypeData = cursor.fetchall()
            return render_template('register.html', userTypeData=userTypeData, positionTypeData=positionTypeData, cityTypeData=cityTypeData)
    else:
        UserDatabase.add_user(request.form['TypeID'], request.form['PositionID'], request.form['BirthCityID'], request.form['No'], request.form['Birthday'], request.form['Name'], request.form['Surname'], request.form['username'], request.form['password'])
        return redirect(url_for('site.home_page'))

@site.route('/contract', methods=['GET', 'POST'])
@login_required
def contract_page():
    if request.method == 'GET':
        contracts = ContractDatabase.GetContractList()
        return render_template('contract.html', contracts = contracts)
    else:
        return redirect(url_for('site.home_page'))

@site.route('/contract/add/', methods=['GET', 'POST'])
@login_required
def contract_add():
    if request.method == 'GET':
        userIDs = UserDatabase.getUserContractAdd()
        print(userIDs)
        return render_template('contract_add.html', UserIDs=userIDs)
    else:
        with dbapi2.connect(database.config) as connection:
            ContractDatabase.add_contract(request.form['UserID'],request.form['Salary'], request.form['SignPremium'], request.form['MatchPremium'], request.form['GoalPremium'], request.form['AssistPremium'], request.form['StartDate'], request.form['EndDate'])
        return redirect(url_for('site.contract_page'))

@site.route('/injury', methods=['GET', 'POST'])
@login_required
def injury_page():
    if request.method == 'GET':
        return render_template('injury.html')
    else:
        InjuryDatabase.add_injury(request.form['RecoveryTime'], request.form['Injury'], request.form['InjuryArea'])

        return redirect(url_for('site.home_page'))
