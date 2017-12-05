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


@site.route('/parameters', methods=['GET', 'POST'])
@login_required
def parameters_page():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()
    if request.method == 'GET':
        #query = """ SELECT P1.NAME FROM PARAMETERS AS P1 JOIN PARAMETERTYPE AS P2 ON(P1.TYPEID=P2.ID) WHERE P2.NAME='City' """
        query = """ SELECT * FROM PARAMETERS"""
        cursor.execute(query)

        all_parameters = cursor.fetchall()

        connection.commit()

        return render_template('parameters.html', user=current_user.username, all_parameters=all_parameters)
    else:

        deletes = request.form.getlist('parameter_to_delete')

        for delete in deletes:
            query = "DELETE FROM PARAMETERS WHERE ID='%d'" % int(delete)
            cursor.execute(query)

        query = """ SELECT * FROM PARAMETERS"""
        cursor.execute(query)

        all_parameters = cursor.fetchall()

        connection.commit()

        return render_template('parameters.html', user=current_user.username, all_parameters=all_parameters)

@site.route('/parameters/add/<int:TYPE>', methods=['GET', 'POST'])
@login_required
def parameter_add(TYPE):
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()

    if request.method == 'GET':
        query = """ SELECT ID,NAME FROM PARAMETERTYPE WHERE ID='%d'"""% TYPE
        cursor.execute(query)
        typeName = cursor.fetchone()


        return render_template('parameter_add.html', user=current_user.username, parameterType=typeName)
    else:
        parameterName = request.form['parameterType']


        query = "INSERT INTO PARAMETERS(TYPEID,NAME) VALUES('%d', '%s')" % (TYPE,parameterName)
        cursor.execute(query)

        connection.commit()

        return redirect(url_for('site.parameters_page'))