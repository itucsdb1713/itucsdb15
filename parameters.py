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
from ParameterCheckDelete import ParamaterCheckDelete

@site.route('/parameters', methods=['GET', 'POST'])
@login_required
def parameters_page():
    if current_user.userType == 'admin':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
        if request.method == 'GET':
            #query = """ SELECT P1.NAME FROM PARAMETERS AS P1 JOIN PARAMETERTYPE AS P2 ON(P1.TYPEID=P2.ID) WHERE P2.NAME='City' """
            query = """ SELECT * FROM PARAMETERS"""
            cursor.execute(query)

            all_parameters = cursor.fetchall()

            connection.commit()

            return render_template('parameters.html', all_parameters=all_parameters)
        else:

            deletes = request.form.getlist('parameter_to_delete')
            print(deletes)

            #### check parameter to be deleted ###
            deletes = ParamaterCheckDelete.search(deletes)

            for delete in deletes:
                query = "DELETE FROM PARAMETERS WHERE ID='%d'" % int(delete)
                cursor.execute(query)

            query = """ SELECT * FROM PARAMETERS"""
            cursor.execute(query)

            all_parameters = cursor.fetchall()

            connection.commit()

            return render_template('parameters.html', all_parameters=all_parameters)
    else:
        return render_template('error.html')

@site.route('/parameters/add/<int:TYPE>', methods=['GET', 'POST'])
@login_required
def parameter_add(TYPE):
    if current_user.userType == 'admin':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

        if request.method == 'GET':
            query = """ SELECT ID,NAME FROM PARAMETERTYPE WHERE ID='%d'"""% TYPE
            cursor.execute(query)
            typeName = cursor.fetchone()


            return render_template('parameter_add.html', parameterType=typeName)
        else:
            parameterName = request.form['parameterType']


            query = "INSERT INTO PARAMETERS(TYPEID,NAME) VALUES('%d', '%s')" % (TYPE,parameterName)
            cursor.execute(query)

            connection.commit()

            return redirect(url_for('site.parameters_page'))
    else:
        return render_template('error.html')


@site.route('/parameters/update/<int:parameterID>', methods=['GET', 'POST'])
@login_required
def parameter_update(parameterID):
    if current_user.userType == 'admin':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':

                query = """ SELECT * FROM PARAMETERS WHERE ID='%d'""" % (parameterID)
                cursor.execute(query)
                parameter = cursor.fetchone()
                query = """ SELECT NAME FROM PARAMETERTYPE WHERE ID='%d'""" % parameter[1]
                cursor.execute(query)
                parameterType = cursor.fetchone()
                connection.commit()

                return render_template('parameter_update.html', parameter=parameter,parameterType=parameterType)
            else:

                new_parameterName = request.form['update_parameter']
                query = """UPDATE Parameters SET Name = '%s' WHERE ID = %d""" % (new_parameterName,parameterID)
                cursor.execute(query)
                connection.commit()
                return redirect(url_for('site.parameters_page'))
    else:
        return render_template('error.html')
