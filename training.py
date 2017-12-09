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


@site.route('/training', methods=['GET', 'POST'])
@login_required
def training_page():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()
        if request.method == 'GET':
            query = """ SELECT y.Name, x.TrainingName, x.Location, x.TrainingDate FROM TrainingInfo As x JOIN Parameters as y ON x.TypeId = y.Id """
            cursor.execute(query)
            trainings = cursor.fetchall()
            connection.commit()
            return render_template('training.html',trainings=trainings)
        else:
            pass  # will be implemented later.

@site.route('/training/add', methods=['GET', 'POST'])
@login_required
def training_add():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()

        if request.method == 'GET':
            query = """ SELECT * FROM PARAMETERS WHERE TYPEID=4"""  #typeid 4 for training
            cursor.execute(query)
            training_data = cursor.fetchall()
            return render_template('training_add.html',training_data=training_data)
        else:
            trainingType = request.form['trainingType']
            trainingName = request.form['trainingName']
            trainingLoc = request.form['trainingLoc']
            trainingDate = request.form['trainingDate']
            
            query = "INSERT INTO TrainingInfo(TYPEID,TrainingName,Location,TrainingDate,CreateUserId,CreateDate) VALUES('%d', '%s', '%s', '%s','%d','%s')" % (int(trainingType), trainingName, trainingLoc, trainingDate,current_user.id,datetime.datetime.now())
            cursor.execute(query)

            connection.commit()

            return redirect(url_for('site.training_page'))