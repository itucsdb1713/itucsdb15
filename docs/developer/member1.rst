Mehmet Taha Çorbacıoğlu Tarafından Yapılan Kısımlar
===================================================

Bütün tablolar create_tables fonksiyonu içerisinde oluşturulmaktadır.

Kullanıcı Giriş Bilgileri
-------------------------

Kullanıcının sisteme giriş yapması için gerekli olan bilgiler "LogInfo" tablosunda tutulmuştur. Bu tabloda kullanıcının UserID birincil anahtar olarak kullanılmıştır. Aynı zamanda UserID, "UserInfo" tablosunu dış anahtar ile bağlamıştır. UserInfo tablosunda UserID serial olduğu ve bu tablodaki UserID ile aynı olduğu için, bu tablodaki UserID integer olarak tutulmuştur. Bu tablo aynı zamanda kullanıcı adı ve şifresini tutmaktadır. Kayıt sırasında şifre hashlenerek saklanmaktadır.

.. code-block:: python

    query = """DROP TABLE IF EXISTS LogInfo CASCADE"""
                cursor.execute(query)
                query = """CREATE TABLE LogInfo (
                                          UserID INT PRIMARY KEY,
                                          Username varchar(50) UNIQUE NOT NULL,
                                          Password varchar(500) NOT NULL,
                                          LastLoginDate TIMESTAMP,
                                          FOREIGN KEY(UserID) REFERENCES UserInfo(UserID)  ON DELETE CASCADE
                                        )"""
                cursor.execute(query)

User sınıfı sisteme o anda giriş yapan kullanıcının bazı bilgilerini tutmaktadır. Aşağıdaki kod parçasında da görüldüğü gibi, bu bilgiler: userID, kullanıcı ismi, şifresi, son giriş zamanı ve kullanıcının tipidir.

.. code-block:: python

    class User(UserMixin):
        def __init__(self, id, username, password, lastLoginDate, userType):
            self.id = id
            self.username = username
            self.password = password
            self.lastLoginDate = lastLoginDate
            self.userType = userType

Ziyaretçi login sayfasına geldiğinde formları doldurarak giriş yapmayı dener. UserDatabase sınıfı içerisinde yer alan select_user fonksiyonu ile forma girilen kullanıcı adı ile veritabanında eşleşen kullanıcıyı çeker. Eğer bu isme sahip bir kullanıcı varsa, forma girilen şifre ile hashlenen şifreyi kontrol eder. Doğru olması koşulunda son giriş zamanını günceller ve Flask-Login kütüphanesinin login_user fonksiyonu ile kullanıcı girişini gerçekleştirir.

.. code-block:: python

    @site.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            user = UserDatabase.select_user(request.form['username'])
            if user and user != -1:
                if pwd_context.verify(request.form['password'], user.password):
                    UserDatabase.setLastLoginDate(user)
                    login_user(user)
                    return redirect(url_for('site.home_page'))

Profil Bilgileri
----------------

Kullanıcıların kişisel bilgileri "UserInfo" tablosunda tutulmaktadır. UserID birincil anahtar olarak kullanılmıştır. UserTypeID, parameters tablosundan kullanıcıyı çekmek için dış anahtar olarak kullanılmıştır. PositionID, parameters tablosundan futbolcunun mevkisini çekmek için dış anahtar olarak kullanılmıştır. CityID, parameters tablosundan kullanıcının doğum yerini çekmek için dış anahtar olarak kullanılmıştır. CreateUserID, kendi tablosuna kullanıcıyı oluşturan kişiyi bulmak için dış anahtar olarak kullanılmıştır.

.. code-block:: python

    query = """DROP TABLE IF EXISTS UserInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE UserInfo (
                                        UserID SERIAL PRIMARY KEY,
                                        UserTypeID INTEGER NOT NULL,
                                        PositionID INTEGER,
                                        CityID INTEGER,
                                        CreateUserID INTEGER NOT NULL,
                                        No INTEGER,
                                        Birthday DATE,
                                        CreateDate TIMESTAMP NOT NULL,
                                        Name VARCHAR(50),
                                        Surname VARCHAR (50),
                                        FOREIGN KEY (UserTypeID) REFERENCES Parameters(ID),
                                        FOREIGN KEY (PositionID) REFERENCES Parameters(ID),
                                        FOREIGN KEY (CityID) REFERENCES Parameters(ID),
                                        FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                        )"""
            cursor.execute(query)

Kullanıcı İşlemleri
-------------------

Kullanıcılar yöneticiler tarafından eklenebilirler. Yöneticiler veya kullanıcılar bilgilerini güncelleyebilir ya da hesaplarını silebilir.

İlk Yöneticinin Oluşturulması
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initdb sayfasına gidildiğinde create_tables fonksiyonu çağrıldıktan sonra adminInit çağrılır ve sistemin ilk yöneticisi veritabanına eklenir. Bunun için ilk önce parametre tablosuna admin kullanıcı tipi eklenir. Ardından boş bir profil yönetici için oluşturulur. Oluşturulan bu profil ile LogInfo tablosuna yöneticinin giriş bilgileri girilir. Burada şifre hash'i alınarak veritabanına kaydedilir.

.. code-block:: python

    def adminInit(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO Parameters(Name,TypeID) VALUES ('admin',1)"""
            cursor.execute(query)

            query= """SELECT ID FROM PARAMETERS WHERE NAME='%s'""" %('admin')
            cursor.execute(query)
            userType = cursor.fetchone()
            query = """INSERT INTO UserInfo(UserTypeID, CreateUserID, CreateDate) VALUES (%s, 1, %s)"""
            cursor.execute(query,(userType,datetime.datetime.now(),))

            query = """SELECT MAX(UserID) FROM UserInfo """
            cursor.execute(query)
            userID = cursor.fetchone()

            hashp = pwd_context.encrypt('12345')
            query = """INSERT INTO LogInfo(UserID, Username, Password) VALUES (%s, 'admin', %s)"""
            cursor.execute(query, (userID[0],hashp,))

            connection.commit()
            cursor.close()

Kullanıcı Eklenmesi
^^^^^^^^^^^^^^^^^^^

Kayıt sayfasında yönetici kontrolü yapılır ardından UserDatabase sınıfından girilen formlara göre yeni bir kullanıcı oluşturmak için add_user fonksiyonu çalıştırılır.

.. code-block:: python

    @site.route('/register', methods=['GET', 'POST'])
    @login_required
    def register_page():
        if current_user.userType == 'admin':
            if request.method == 'GET':
                with dbapi2.connect(database.config) as connection:
                    cursor = connection.cursor()
                    query = """ SELECT * FROM PARAMETERS WHERE TYPEID=1"""  # typeid 1 for user type
                    cursor.execute(query)
                    userTypeData = cursor.fetchall()
                    query = """ SELECT * FROM PARAMETERS WHERE TYPEID=2"""  # typeid 2 for position type
                    cursor.execute(query)
                    positionTypeData = cursor.fetchall()
                    query = """ SELECT * FROM PARAMETERS WHERE TYPEID=3"""  # typeid 3 for city type
                    cursor.execute(query)
                    cityTypeData = cursor.fetchall()
                    return render_template('register.html', userTypeData=userTypeData, positionTypeData=positionTypeData, cityTypeData=cityTypeData)
            else:
                UserDatabase.add_user(request.form['TypeID'], request.form['PositionID'], request.form['BirthCityID'], request.form['No'], request.form['Birthday'], request.form['Name'], request.form['Surname'], request.form['username'], request.form['password'])
                return redirect(url_for('site.home_page'))
        else:
            return render_template('error.html')

Formdan gelen bilgiler ile ilk önce UserInfo tablosuna yeni bir satır eklenir. Ardından giriş bilgileri için LogInfo tablasuna eklenme yapılır. Eğer futbolcu kaydı yapılıyorsa istatistik tablosuna da ekleme yapılır.

.. code-block:: python

    class UserDatabase:
        @classmethod
        def add_user(cls, TypeID, PositionID, BirthCityID, No, Birthday, Name, Surname, username, password):
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO UserInfo (UserTypeID, PositionID, CityID, CreateUserID, No, Birthday,
                                                                  CreateDate, Name, Surname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                try:
                    cursor.execute(query, (str(TypeID), str(PositionID), str(BirthCityID), str(current_user.id), str(No), Birthday, datetime.datetime.now(), Name, Surname))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                query = """SELECT MAX(UserID) FROM UserInfo """
                try:
                    cursor.execute(query)
                except dbapi2.Error:
                    connection.rollback()
                else:
                    userID = cursor.fetchone()
                    connection.commit()
                hashp = pwd_context.encrypt(password)
                query = """INSERT INTO LogInfo (userID, Username, Password) VALUES ('%d','%s','%s')"""%(userID[0], username, hashp)

                try:
                    cursor.execute(query)
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                query = """SELECT name FROM Parameters WHERE ID = '%s' """%(TypeID)
                try:
                    cursor.execute(query)
                except dbapi2.Error:
                    connection.rollback()
                else:
                    parameterName = cursor.fetchone()
                    connection.commit()

                if parameterName[0] == 'Footballer':
                    query = """INSERT INTO StatisticsInfo (ID) VALUES ('%s')"""%(str(userID[0]))
                    try:
                        cursor.execute(query)
                    except dbapi2.Error:
                        connection.rollback()
                    else:
                        connection.commit()

                cursor.close()

Kullanıcı Bilgilerinin Güncellenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Profil güncellemek için istek geldiğinde kullanıcı numarası üzerinden kullanıcın bilgileri güncellenir.

.. code-block:: python

    @classmethod
    def updateUser(cls, currentId, newName, newSurname, newType, newNo, newBirthday, newPosition, newCity):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            try:
                if(newName != ''):
                    query = "UPDATE USERINFO SET name='%s' WHERE userid = '%d'" % (newName, int(currentId))
                    cursor.execute(query)
                if(newSurname != ''):
                    query = "UPDATE USERINFO SET surname='%s' WHERE userid = '%d'" % (newSurname, int(currentId))
                    cursor.execute(query)
                if(newType != ''):
                    query = "UPDATE USERINFO SET usertypeid='%d' WHERE userid = '%d'" % (int(newType), int(currentId))
                    cursor.execute(query)
                if(newNo != ''):
                    query = "UPDATE USERINFO SET no='%d' WHERE userid = '%d'" % (int(newNo), int(currentId))
                    cursor.execute(query)
                if(newBirthday != ''):
                    query = "UPDATE USERINFO SET birthday='%s' WHERE userid = '%d'" % (newBirthday, int(currentId))
                    cursor.execute(query)
                if(newPosition != ''):
                    query = "UPDATE USERINFO SET positionid='%d' WHERE userid = '%d'" % (int(newPosition), int(currentId))
                    cursor.execute(query)
                if(newCity !=''):
                    query = "UPDATE USERINFO SET cityid='%d' WHERE userid = '%d'" % (int(newCity), int(currentId))
                    cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

Kullanıcının Silinmesi
^^^^^^^^^^^^^^^^^^^^^^

Silme isteği geldiğinde kullanıcı numarası üzerinden UserInfo tablosunda silme gerçekleştirilir. Bu tablodan bir kullanıcının silinmesi LogInfo ve diğer bağlantılı tablolardaki verilerin de silinmesini sağlar.

.. code-block:: python

    @classmethod
    def deleteUser(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            try:
                query = "DELETE FROM USERINFO WHERE USERID = '%d' " % int(ID)
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

Futbolcular için Sakatlık Bilgisi
---------------------------------

Sakatlık tablosunda ID birincil anahtar olarak kullanılmaktadır. UserID, UserInfo tablosuna dış anahtar olarak bağlanmıştır ve buradan hangi futbolcuya ait sakatlığın girildiği belirtilmektedir. CreateUserID ise yine UserInfo tablosuna dış anahtardır ve sakatlığın kim tarafından girildiğini göstermektedir.

.. code-block:: python

    query = """DROP TABLE IF EXISTS InjuryInfo CASCADE"""
                cursor.execute(query)
                query = """CREATE TABLE InjuryInfo (
                                          ID SERIAL PRIMARY KEY,
                                          UserID INTEGER NOT NULL,
                                          RecoveryTime INTEGER NOT NULL,
                                          CreateUserID INTEGER NOT NULL,
                                          CreateDate TIMESTAMP NOT NULL,
                                          Injury VARCHAR(500) NOT NULL,
                                          InjuryArea VARCHAR(50) NOT NULL,
                                          FOREIGN KEY (UserID) REFERENCES UserInfo(UserID),
                                          FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                        )"""
                cursor.execute(query)

Sakatlık Bilgisinin Eklenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sakatlık bilgisi eklenirken formdan gelen bilgiler add_injury fonksiyonuna gönderilir ve veritabanına burada ekleme yapılır.

.. code-block:: python

    @classmethod
    def add_injury(cls,UserID, RecoveryTime, Injury, InjuryArea):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            CreateDate = datetime.datetime.now()
            CreateUserID = current_user.id
            query = """INSERT INTO InjuryInfo (UserID, RecoveryTime, CreateUserID, CreateDate, Injury, InjuryArea) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (UserID, RecoveryTime, CreateUserID, CreateDate, Injury, InjuryArea,))
            cursor.close()

Sakatlık Bilgisinin Güncellenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sakatlık bilgisi güncellenirken id'si üzerinden veritabanından bulunan sakatlık bilgisi formdan gelen bilgiler ile güncellenir.


.. code-block:: python

    @classmethod
    def update_injury(cls, ID, RecoveryTime, Injury, InjuryArea):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM InjuryInfo WHERE ID = %d""" % (ID)
            cursor.execute(query)
            injuryInfo = cursor.fetchone()
            injury = list(injuryInfo)
            if RecoveryTime != "":
                injury[2] = RecoveryTime
            if Injury != "":
                injury[5] = Injury
            if InjuryArea != "":
                injury[6] = InjuryArea

            query = """UPDATE InjuryInfo
                            SET RecoveryTime = '%s', Injury= '%s', InjuryArea= '%s'
                            WHERE ID = %d """ % (injury[2], injury[5], injury[6], ID)
            cursor.execute(query)
            cursor.close()

Sakatlık Bilgisinin Silinmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Id'si ile veritabanında bulduğumuz sakatlık bilgisi silinir.

.. code-block:: python

    @classmethod
    def DeleteInjury(cls,ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM InjuryInfo WHERE ID = %s"""%(ID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

Kontrat Bilgileri
-----------------

Kontrat tablosunda ID birincil anahtar olarak kullanılmaktadır. UserID, UserInfo tablosuna dış anahtar olarak bağlanmıştır ve buradan hangi futbolcuya ait kontratın girildiği belirtilmektedir. CreateUserID ise yine UserInfo tablosuna dış anahtardır ve kontratı kimin imzaladığı tutulmaktadır.

.. code-block:: python

    query = """DROP TABLE IF EXISTS ContractInfo CASCADE"""
                cursor.execute(query)

                query = """CREATE TABLE ContractInfo (
                                                    ID SERIAL PRIMARY KEY,
                                                    UserID INTEGER NOT NULL,
                                                    CreateUserID INTEGER NOT NULL,
                                                    Salary DECIMAL DEFAULT 0,
                                                    SignPremium DECIMAL DEFAULT 0,
                                                    MatchPremium DECIMAL DEFAULT 0,
                                                    GoalPremium DECIMAL DEFAULT 0,
                                                    AssistPremium DECIMAL DEFAULT 0,
                                                    SignDate TIMESTAMP NOT NULL,
                                                    EndDate TIMESTAMP NOT NULL,
                                                    CreateDate TIMESTAMP NOT NULL,
                                                    FOREIGN KEY (UserID) REFERENCES UserInfo(UserID),
                                                    FOREIGN KEY (CreateUserID) REFERENCES UserInfo(UserID)
                                                    )"""

                cursor.execute(query)

Kontrat Bilgilerinin Eklenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kontrat bilgisi eklenirken formdan gelen bilgiler add_contract fonksiyonuna gönderilir ve veritabanına burada ekleme yapılır.

.. code-block:: python

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

Kontrat Bilgilerinin Güncellenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kontrat bilgisi güncellenirken id'si üzerinden veritabanından bulunan sakatlık bilgisi formdan gelen bilgiler ile güncellenir.

.. code-block:: python

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

Kontrat Bilgilerinin Silinmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Id'si ile veritabanında bulduğumuz kontrat bilgisi silinir.


.. code-block:: python

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

İstatistik Bilgileri
--------------------

İstatistik tablosunda ID birincil anahtar olarak kullanılmaktadır. UserID, UserInfo tablosuna dış anahtar olarak bağlanmıştır ve buradan hangi futbolcuya ait istatistiğin girildiği belirtilmektedir.

.. code-block:: python

    query = """DROP TABLE IF EXISTS StatisticsInfo CASCADE"""
                cursor.execute(query)

                query = """CREATE TABLE StatisticsInfo (
                                                                    ID INT PRIMARY KEY,
                                                                    Goal INTEGER DEFAULT 0,
                                                                    Assist INTEGER DEFAULT 0,
                                                                    Match INTEGER DEFAULT 0,
                                                                    FOREIGN KEY(ID) REFERENCES UserInfo(UserID)  ON DELETE CASCADE
                                                                    )"""
                cursor.execute(query)

İstatistik Bilgilerinin Eklenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

İstatistik bilgisi eklenirken formdan gelen bilgiler add_statistics fonksiyonuna gönderilir ve veritabanına burada ekleme yapılır.

.. code-block:: python

    @classmethod
    def add_statistics(cls, ID, Goal, Asist, Match):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM StatisticsInfo WHERE ID = %s""" % (ID)
            cursor.execute(query)
            statisticsInfo = cursor.fetchone()
            statistics = list(statisticsInfo)
            if Goal != "":
                statistics[1] = int(Goal) + int(statistics[1])
            if Asist != "":
                statistics[2] = int(Asist) + int(statistics[2])
            if Match != "":
                statistics[3] = int(Match) + int(statistics[3])

            query = """UPDATE StatisticsInfo
                            SET Goal = '%s', Assist= '%s', Match= '%s'
                            WHERE ID = '%s' """ % (str(statistics[1]), str(statistics[2]), str(statistics[3]), str(ID))
            cursor.execute(query)
            cursor.close()

İstatistik Bilgilerinin Güncellenmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

İstatistik bilgisi güncellenirken id'si üzerinden veritabanından bulunan istatistik bilgisi formdan gelen bilgiler ile güncellenir.

.. code-block:: python

    @classmethod
    def update_statistics(cls, ID, Goal, Assist, Match):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM StatisticsInfo WHERE ID = %d""" % (ID)
            cursor.execute(query)
            statisticsInfo = cursor.fetchone()
            statistics = list(statisticsInfo)
            if Goal != "":
                statistics[1] = Goal
            if Assist != "":
                statistics[2] = Assist
            if Match != "":
                statistics[3] = Match

            query = """UPDATE StatisticsInfo
                                SET Goal = '%s', Assist= '%s', Match= '%s'
                                WHERE ID = %d """ % (statistics[1], statistics[2], statistics[3], ID)
            cursor.execute(query)
            cursor.close()

İstatistik Bilgilerinin Silinmesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Id'si ile veritabanında bulduğumuz istatistik bilgisi silinir.

.. code-block:: python

    @classmethod
    def DeleteStatistic(cls, ID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """UPDATE StatisticsInfo
                                            SET Goal = %d, Assist= %d, Match= %d
                                            WHERE ID = '%s' """ % (0, 0, 0, ID)
            cursor.execute(query)
            cursor.close()