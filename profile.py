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

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    if request.method == 'GET':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = "SELECT usertypeid FROM userinfo WHERE userid='%d'" %int(current_user.id)
            cursor.execute(query)
            usertype = cursor.fetchone()
            if(usertype[0] == 95):
                query = "SELECT name, surname, userid FROM userinfo"
                cursor.execute(query)
                users = cursor.fetchall()
                return render_template('profile.html', usertype=usertype[0], users=users)
            else:
                return render_template('profile.html')
    else:
        return redirect(url_for('site.profile_edit_page', userid=int(request.form['User'])))

@site.route('/profile-edit/<int:userid>', methods=['GET', 'POST'])
@login_required
def profile_edit_page(userid):
    if request.method == 'GET':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = "SELECT x.name, x.surname, y.name, x.no, x.birthday FROM userinfo as x JOIN parameters as y on (y.id=x.usertypeid OR y.id=x.cityid OR y.id = x.positionid) WHERE x.userid ='%d'" % int(userid)
            cursor.execute(query)
            user = cursor.fetchall()
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=1"""  # typeid 1 for user type
            cursor.execute(query)
            userTypeData = cursor.fetchall()
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=2"""  # typeid 2 for position type
            cursor.execute(query)
            positionTypeData = cursor.fetchall()
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=3"""  # typeid 3 for city type
            cursor.execute(query)
            cityTypeData = cursor.fetchall()
            return render_template('profile_edit.html', id= userid,user=user, userTypeData=userTypeData, positionTypeData=positionTypeData, cityTypeData=cityTypeData)
    else:
        UserDatabase.updateUser(userid, request.form['Name'], request.form['Surname'], request.form['Type'], request.form['No'], request.form['Birthday'], request.form['Position'], request.form['City'])
        return redirect(url_for('site.profile_page'))