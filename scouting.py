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

            return render_template('scouting.html')




