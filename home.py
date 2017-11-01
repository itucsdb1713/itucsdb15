from handlers import site
from database import database
from user import *

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
    print(current_user.username)
    return render_template('home.html', current_time=now.ctime())

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
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        UserDatabase.add_user(request.form['username'], request.form['password'])
        return redirect(url_for('site.home_page'))