import psycopg2 as dbapi2
import json
import re
import os
from passlib.apps import custom_app_context as pwd_context

class DatabaseOPS:
    def __init__(self):

        VCAP_SERVICES = os.getenv('VCAP_SERVICES')

        if VCAP_SERVICES is not None:
            self.config = DatabaseOPS.get_elephantsql_dsn(VCAP_SERVICES)
        else:
            self.config = """user='postgres' password='12345'
                            host='localhost' port=5432 dbname='beeINfootball'"""

    @classmethod
    def get_elephantsql_dsn(cls, vcap_services):
        """Returns the data source name for ElephantSQL."""
        parsed = json.loads(vcap_services)
        uri = parsed["elephantsql"][0]["credentials"]["uri"]
        match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
        user, password, host, _, port, dbname = match.groups()
        dsn = """user='{}' password='{}' host='{}' port={}
                 dbname='{}'""".format(user, password, host, port, dbname)
        return dsn

    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS USERS (
                                      USER_ID SERIAL PRIMARY KEY,
                                      USERNAME varchar(20) UNIQUE NOT NULL,
                                      PASSWORD varchar NOT NULL
                                    )"""
            cursor.execute(query)
            hashp = pwd_context.encrypt('123')
            query = """INSERT INTO USERS(USERNAME, PASSWORD) VALUES ('taha', %s)"""
            cursor.execute(query, (hashp,))
            connection.commit()
            cursor.close()

database = DatabaseOPS()