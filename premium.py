import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user


class PremiumDatabase:
    @classmethod
    def add_premium(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            CreateUserID = current_user.id
            query = """SELECT ID, Goal, Assist, Match FROM StatisticsInfo"""
            try:
                cursor.execute(query)
                statisticsInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            statistics = list(statisticsInfo)

            query = """SELECT UserID, GoalPremium, AssistPremium, MatchPremium, SignPremium, Salary FROM ContractInfo"""
            try:
                cursor.execute(query)
                contractInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            query = """SELECT * FROM PremiumInfo"""
            try:
                cursor.execute(query)
                premiumInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            query = """SELECT ID, Name  FROM Parameters WHERE TypeID = 5"""
            try:
                cursor.execute(query)
                parameterInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            contracts = list(contractInfo)
            statistics = list(statisticsInfo)
            parameters = list(parameterInfo)
            premiums = list(premiumInfo)

            for i in statistics:
                for j in contracts:
                    ctrl = False
                    if i[0] == j[0]:
                        for m in premiums:
                            if m[0] == i[0]:
                                ctrl = True
                                break
                        for k in range(1, 6):
                            if k < 4:
                                userID = i[0]
                                amount = j[k] * i[k]
                                if k == 1:
                                    for l in parameters:
                                        if l[1] == 'Goal Premium':
                                            type = l[0]
                                if k == 2:
                                    for l in parameters:
                                        if l[1] == 'Assist Premium':
                                            type = l[0]
                                if k == 3:
                                    for l in parameters:
                                        if l[1] == 'Match Premium':
                                            type = l[0]
                            else:
                                if k == 4:
                                    for l in parameters:
                                        if l[1] == 'Sign Premium':
                                            type = l[0]
                                            amount = j[k]
                                if k == 5:
                                    for l in parameters:
                                        if l[1] == 'Salary':
                                            type = l[0]
                                            amount = j[k]

                            if ctrl == True:
                                query = """UPDATE  PremiumInfo SET Amount = %d WHERE UserID = %s and PremiumTypeID = %s """ % (
                                    amount, userID, type)
                            else:
                                query = """INSERT INTO PremiumInfo (UserID, PremiumTypeID, Amount, CreateUserID, CreateDate) 
                                        VALUES ('%s', '%s', '%s', '%s', '%s')""" % (
                                    str(userID), str(type), str(amount), str(CreateUserID), datetime.datetime.now())
                            try:
                                cursor.execute(query)
                            except dbapi2.Error:
                                connection.rollback()
                            else:
                                connection.commit()
            cursor.close()

    @classmethod
    def getPremiums(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT k.UserID, m.name, m.surname , l.name, k.Amount FROM UserInfo as m, PremiumInfo as k, Parameters as l WHERE m.UserID = k.UserID and k.PremiumTypeID = l.ID"""
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                premiumInfo = cursor.fetchall()
                connection.commit()
            query = """SELECT ID, Name  FROM Parameters WHERE TypeID = 5"""
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                parameterInfo = cursor.fetchall()
                connection.commit()
            parameters = list(parameterInfo)

            premiums1 = list(premiumInfo)
            premiums2 = list(premiumInfo)
            count = len(premiums1)
            counter = 0
            premiumList = []
            tempPremium = []
            premium = []
            for i in premiums1:
                if counter %5 == 0:
                    premium.append(i[0])
                    premium.append(i[1])
                    premium.append(i[2])
                if i[3] == 'Goal Premium':
                    premium.insert(5, i[4])
                if i[3] == 'Assist Premium':
                    premium.insert(6, i[4])
                if i[3] == 'Match Premium':
                    premium.insert(7, i[4])
                if i[3] == 'Sign Premium':
                    premium.insert(4, i[4])
                if i[3] == 'Salary':
                    premium.insert(3, i[4])
                if counter %5 == 4:
                    premiumList.append(premium)
                    premium = []
                counter = counter + 1

        return premiumList

    @classmethod
    def DeletePremium(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            print("ID",ID)
            query = "DELETE FROM PremiumInfo WHERE userID='%d'" % int(ID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                print("Rollback")
                connection.rollback()

            else:
                print("commit")
                connection.commit()
            cursor.close()
            return
            # or j in range(counter + 1, count - 1):
    #   if i[0] == premiums2[j][0]:
    #       if i[3] == 'Goal Premium':
    #           print("Goal 2")

    #           premium.insert(5, i[4])
    #           break
    #       if i[3] == 'Assist Premium':
    #           print("Assist 2")

    #           premium.insert(6, i[4])
    #           break
    #       if i[3] == 'Match Premium':
    #           print("Match 2")

    #           premium.insert(7, i[4])
    #           break
    #       if i[3] == 'Sign Premium':
    #           print("Sign 2")

    #           premium.insert(4, i[4])
    #           break
    #       if i[3] == 'Salary':
    #           print("Salary 2")

    #           premium.insert(3, i[4])
    ##           break
