import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user


class ParamaterCheckDelete:

    @classmethod
    def search(self, parameters):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            print("parameters", parameters)
            deletes = []
            for parameter in parameters:
                ID, TypeID = parameter.split(",",1)


                if TypeID == '1':
                    query = """ SELECT COUNT(*) FROM UserInfo WHERE UserTypeID = %d """ %(int(ID))
                    cursor.execute(query)
                    userTypeCount = cursor.fetchone()[0]

                    if userTypeCount == 0:
                        deletes.append(ID)
                if TypeID == '2':
                    query = """ SELECT COUNT(*) FROM UserInfo WHERE UserTypeID = %d """ %(int(ID))
                    cursor.execute(query)
                    positionTypeCount = cursor.fetchone()[0]

                    if positionTypeCount == 0:
                        deletes.append(ID)
                if TypeID == '3':
                    query = """ SELECT COUNT(*) FROM UserInfo WHERE CityID = %d""" %(int(ID))
                    cursor.execute(query)
                    cityTypeCount = cursor.fetchone()[0]
                    query = """ SELECT COUNT(*) FROM FixtureInfo WHERE CityID = %d""" % (int(ID))
                    cursor.execute(query)
                    cityTypeCount = cityTypeCount + cursor.fetchone()[0]

                    if cityTypeCount == 0:
                        deletes.append(ID)


                if TypeID == '4':
                    query = """ SELECT COUNT(*) FROM TrainingInfo WHERE TypeID = %d """ %(int(ID))
                    cursor.execute(query)
                    trainingTypeCount = cursor.fetchone()[0]

                    if trainingTypeCount == 0:
                        deletes.append(ID)

                if TypeID == '5':
                    query = """ SELECT COUNT(*) FROM PremiumInfo WHERE PremiumTypeID = %d """ %(int(ID))
                    cursor.execute(query)
                    premiumTypeCount = cursor.fetchone()[0]

                    if premiumTypeCount == 0:
                        deletes.append(ID)

            connection.commit()
            return deletes

