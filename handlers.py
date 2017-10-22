from flask import redirect
from flask import url_for
from flask import Blueprint

from database import database

site = Blueprint('site',__name__)

@site.route('/initdb')
def initialize_database():
    database.create_tables()
    return redirect(url_for('site.home_page'))

