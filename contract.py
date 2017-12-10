import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user

class Contract():
    def __init__(self, ID, userID, createUserID, salary, signPremium, matchPremium, goalPremium, assistPremium, signDate, endDate, createDate):
        self.ID = ID
        self.userID = userID
        self.createUserID = createUserID
        self.salary = salary
        self.signPremium = signPremium
        self.matchPremium = matchPremium
        self.goalPremium = goalPremium
        self.assistPremium = assistPremium
        self.signDate = signDate
        self.endDate = endDate
        self.createDate = createDate

class ContractDatabase:
    @classmethod
    def add_contract(cls, ID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, SignDate, EndDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            CreateUserID = current_user.id
            query = """INSERT INTO ContractInfo (UserID, CreateUserID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, 
                                                              SignDate, EndDate, CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (ID, CreateUserID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium,
                                                              SignDate, EndDate, CreateDate,))
            cursor.close()


    @classmethod
    def update_contract(cls, ID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, SignDate, EndDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM ContractInfo WHERE ID = %d"""%(ID)
            cursor.execute(query)
            contractInfo = cursor.fetchone()
            contract = list(contractInfo)
            if Salary != "":
                contract[3] = Salary
            if SignPremium != "":
                contract[4] = SignPremium
            if MatchPremium != "":
                contract[5] = MatchPremium
            if GoalPremium != "":
                contract[6] = GoalPremium
            if AssistPremium != "":
                contract[7] = AssistPremium
            if SignDate != "":
                contract[8] = SignDate
            if EndDate != "":
                contract[9] = EndDate

            query = """UPDATE ContractInfo 
                        SET Salary = '%s', SignPremium= '%s', MatchPremium= '%s', GoalPremium= '%s', AssistPremium= '%s', SignDate= '%s', EndDate= '%s'
                        WHERE ID = %d """ %(contract[3], contract[4], contract[5], contract[6], contract[7], contract[8], contract[9], ID)
            cursor.execute(query)
            cursor.close()

    @classmethod
    def GetContractInfo(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT k.ID, l.name, l.surname, k.Salary, k.SignPremium , k.MatchPremium , k.GoalPremium , k.AssistPremium, k.SignDate, k.EndDate
                                    FROM ContractInfo as k, UserInfo as l, Parameters as m 
                                    WHERE k.UserID = l.UserID and l.UserTypeID = m.ID and k.ID = %s"""%(ID)
            try:
                cursor.execute(query)
                contractInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return contractInfo

    @classmethod
    def GetContractInfoUser(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT k.Salary, k.SignPremium , k.MatchPremium , k.GoalPremium , k.AssistPremium, k.SignDate, k.EndDate
                                        FROM ContractInfo as k, UserInfo as l, Parameters as m 
                                        WHERE k.UserID = l.UserID and l.UserTypeID = m.ID and k.userID = %s""" % (ID)
            try:
                cursor.execute(query)
                contractInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return contractInfo

    @classmethod
    def GetContractList(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT k.ID, m.name, l.name, l.surname, k.salary, k.signpremium, k.matchpremium, k.goalpremium, k.assistpremium, k.SignDate, k.EndDate
                        FROM ContractInfo as k, UserInfo as l, Parameters as m 
                        WHERE k.UserID = l.UserID and l.UserTypeID = m.ID"""

            try:
                cursor.execute(query)
                contractInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return contractInfo

    @classmethod
    def DeleteContract(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM ContractInfo WHERE ID = %s"""%(ID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
