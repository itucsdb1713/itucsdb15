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
    def add_contract(cls, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, SignDate, EndDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            UserID = 1
            CreateUserID = 1
            query = """INSERT INTO ContractInfo (UserID, CreateUserID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium, 
                                                              SignDate, EndDate, CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (UserID, CreateUserID, Salary, SignPremium, MatchPremium, GoalPremium, AssistPremium,
                                                              SignDate, EndDate, CreateDate,))
            cursor.close()

    @classmethod
    def GetContractInfo(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT TOP 1 * FROM LogInfo WHERE UserID=%s Order By CreateDate desc"""

            try:
                cursor.execute(query, (userID,))
                contractInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if contractInfo:
                return Contract(ID = contractInfo[0], userID = contractInfo[1], createUserID = contractInfo[2], salary = contractInfo[3], signPremium = contractInfo[4], matchPremium = contractInfo[5], goalPremium = contractInfo[6], assistPremium = contractInfo[7], signDate = contractInfo[8], endDate = contractInfo[9], createDate=contractInfo[10])
            else:
                return -1