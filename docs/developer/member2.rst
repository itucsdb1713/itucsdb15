Ufuk Şahar Tarafından Yapılan Kısımlar
======================================

Antrenman Bilgisi
-----------------

- Antrenman bilgisi tablosu
   Bu tabloda antrenman ile ilgili bilgiler yer almakta ve antrenman tipi(TypeID) dış anahtarı ile parametreler tablosuna başvuru yapıp parametre tablosunda var olan antrenman tiplerini kullanabiliriz. Ayrıca, antrenmanı ekleyen kullanıcı(CreateUserID) dış anahtarı ile kullanıcı bilgisi tablosuna başvuru yapıp antrenmanı kimin eklediği bilgisine ulaşabiliriz.

- Antrenman bilgisi ekleme

.. code-block:: python

    def training_add():
        if current_user.userType == 'admin' or current_user.userType == 'Trainer':
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
        else:
            return render_template('error.html')


- Antrenman bilgisi güncelleme

.. code-block:: python

    def training_update(trainingID):
        if current_user.userType == 'admin' or current_user.userType == 'Trainer':
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                    if new_trainingType != '':
                        query = """UPDATE TrainingInfo SET TypeID = '%s' WHERE ID = %d""" % (new_trainingType, int(trainingID))
                        cursor.execute(query)
                    if new_trainingName != '':
                        query = """UPDATE TrainingInfo SET TrainingName = '%s' WHERE ID = %d""" % (new_trainingName, int(trainingID))
                        cursor.execute(query)
                    if new_trainingLoc != '':
                        query = """UPDATE TrainingInfo SET Location = '%s' WHERE ID = %d""" % (new_trainingLoc, int(trainingID))
                        cursor.execute(query)
                    if new_trainingDate != '':
                        query = """UPDATE TrainingInfo SET TrainingDate = '%s' WHERE ID = %d""" % (new_trainingDate, int(trainingID))
                        cursor.execute(query)


                    connection.commit()
                    return redirect(url_for('site.training_page'))
        else:
            return render_template('error.html')


- Antrenman bilgisi silme

.. code-block:: python

    def training_page():
        if current_user.userType == 'admin' or current_user.userType == 'Trainer':
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                deletes = request.form.getlist('training_to_delete')

                for delete in deletes:
                    query = "DELETE FROM TrainingInfo WHERE ID='%d'" % int(delete)
                    cursor.execute(query)


                return redirect(url_for('site.training_page'))
        else:
            return render_template('error.html')



Maç Bilgisi
-------------------------
- Maç bilgisi tablosu
   Bu tabloda gerekli maç bilgileri yer almakta ve şehir(cityID) dış anahtarı ile parametre tablosuna başvuru yapıp parametre tablosunda var olan şehir bilgilerini kullanabiliriz.

- Maç bilgisi ekleme

.. code-block:: python

    def fixture_add():
        if current_user.userType == 'admin':
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                if request.method == 'GET':
                    query = """ SELECT * FROM PARAMETERS WHERE TYPEID=3"""  # typeid 3 for city
                    cursor.execute(query)
                    city_data = cursor.fetchall()
                    return render_template('fixture_add.html', city_data=city_data)
                else:
                    fixtureHomeName = request.form['fixtureHomeName']
                    fixtureAwayName = request.form['fixtureAwayName']
                    fixtureArena = request.form['fixtureArena']
                    fixtureCity = request.form['fixtureCity']
                    matchDate = request.form['matchDate']


                    query = "INSERT INTO FixtureInfo(CityID,HomeTeamName,AwayTeamName,ArenaName,matchDate) VALUES('%d', '%s', '%s', '%s','%s')" % (
                    int(fixtureCity), fixtureHomeName, fixtureAwayName, fixtureArena, matchDate)
                    cursor.execute(query)

                    connection.commit()

                    return redirect(url_for('site.fixture_page'))
        else:
            return render_template('error.html')

- Maç bilgisi güncelleme

.. code-block:: python

    def fixture_update(matchID):
        if current_user.userType == 'admin':
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                new_Home = request.form['fixtureHomeName']
                new_Away = request.form['fixtureAwayName']
                new_Arena = request.form['fixtureArena']
                new_HomeScore = request.form['fixtureHomeScore']
                new_AwayScore = request.form['fixtureAwayScore']
                new_City = request.form['fixtureCity']
                new_Date = request.form['matchDate']
                query = """SELECT * FROM FixtureInfo WHERE ID = %d""" % (matchID)
                cursor.execute(query)
                fixtureInfo = cursor.fetchone()
                fixture = list(fixtureInfo)
                if new_Home != "":
                fixture[5] = new_Home
                if new_Away != "":
                fixture[6] = new_Away
                if new_Arena != "":
                fixture[7] = new_Arena
                if new_HomeScore != "":
                fixture[2] = new_HomeScore
                if new_AwayScore != "":
                fixture[3] = new_AwayScore
                if new_City != "":
                fixture[1] = new_City
                if new_Date != "":
                fixture[4] = new_Date
                query = """UPDATE FixtureInfo SET HomeTeamName = '%s', AwayTeamName= '%s', ArenaName= '%s', CityID= '%d', HomeTeamScore= '%s', AwayTeamScore= '%s', MatchDate= '%s'
                WHERE ID = %d """ % (
                fixture[5], fixture[6], fixture[7], int(fixture[1]), fixture[2], fixture[3], fixture[4], matchID)
                cursor.execute(query)
                cursor.close()
                connection.commit()
                return redirect(url_for('site.fixture_page'))

- Maç bilgisi silme

.. code-block:: python

    def fixture_page():
        if current_user.userType == 'admin':
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                if request.method == 'GET':
                    query = """ SELECT x.ID, x.HomeTeamName, x.AwayTeamName, x.ArenaName, y.Name, x.HomeTeamScore, x.AwayTeamScore, x.Matchdate FROM FixtureInfo As x JOIN Parameters as y ON x.CityId = y.Id ORDER BY x.MatchDate DESC"""
                    cursor.execute(query)
                    fixture = cursor.fetchall()
                    connection.commit()
                    return render_template('fixture.html', fixture=fixture)
                else:
                    deletes = request.form.getlist('fixture_to_delete')

                    for delete in deletes:
                        query = "DELETE FROM FixtureInfo WHERE ID='%d'" % int(delete)
                        cursor.execute(query)
                    return redirect(url_for('site.fixture_page'))
        else:
            return render_template('error.html')

.. code-block:: python


Gözlenen Futbolcular
----------------------------

- Gözlenen oyuncu bilgisi tablosu
   Bu tabloda gözlenen futbolcular ile ilgili bilgiler yer almakta ve gözlemci(ScoutID) dış anahtarı ile kullanıcılar tablosuna başvuru yapıp gözlemci bilgisine erişebiliriz. Ayrıca, maç bilgisi(MatchID) dış anahtarı ile maç bilgisi tablosuna başvuru yapıp gözlenen oyuncunun hangi maçta izlendiği bilgisine erişebiliriz.

- Gözlenen futbolcuları ekleme

.. code-block:: python

    def scouting_add():
        if current_user.userType == 'admin' or current_user.userType == "Scout":
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                if request.method == 'GET':
                    query = """ SELECT * FROM FixtureInfo"""
                    cursor.execute(query)
                    match_data = cursor.fetchall()
                    return render_template('scouting_add.html', match_data=match_data)

                else:
                    matchType = request.form['matchType']
                    observedName = request.form['observedName']
                    observedSurname = request.form['observedSurname']
                    observedPoint = request.form['observedPoint']
                    if observedPoint == '':
                        observedPoint = 0
                    query = "INSERT INTO ObservedPlayerInfo(MatchID, ScoutID, Name, Surname, Point,CreateDate) VALUES('%d', '%d', '%s', '%s','%d','%s')" % (int(matchType), current_user.id, observedName, observedSurname, int(observedPoint), datetime.datetime.now())
                    cursor.execute(query)

                    connection.commit()

                    return redirect(url_for('site.scouting_page'))
        else:
            return render_template('error.html')

- Gözlenen futbolcuları güncelleme

.. code-block:: python

    def scouting_update(observedID):
        if current_user.userType == 'admin' or current_user.userType == "Scout":
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                new_Match = request.form['matchType']
                new_Name = request.form['observedName']
                new_Surname = request.form['observedSurname']
                new_Point = request.form['observedPoint']
                new_Date = datetime.datetime.now()
                query = """SELECT * FROM ObservedPlayerInfo WHERE ID = %d""" % (observedID)
                cursor.execute(query)
                observedPlayerInfo = cursor.fetchone()
                observedPlayer = list(observedPlayerInfo)
                if new_Name != "":
                observedPlayer[5] = new_Name
                if new_Surname != "":
                observedPlayer[6] = new_Surname
                if new_Point != "":
                observedPlayer[3] = new_Point
                query = """UPDATE ObservedPlayerInfo
                SET Name = '%s', Surname= '%s', Point= '%s', MatchID= '%d', CreateDate= '%s'
                WHERE ID = %d """ % (
                observedPlayer[5], observedPlayer[6], observedPlayer[3], int(new_Match),new_Date, observedID)
                cursor.execute(query)
                cursor.close()
                connection.commit()
                return redirect(url_for('site.scouting_page'))
        else:
            return render_template('error.html')

- Gözlenen futbolcuları silme

.. code-block:: python

    def scouting_page():
        if current_user.userType == 'admin' or current_user.userType == "Scout":
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                if request.method == 'GET':
                    query = """ SELECT x.ID, x.Name, x.Surname, x.Point, x.CreateDate, y.HomeTeamName, y.AwayTeamName, y.ArenaName, y.MatchDate  FROM ObservedPlayerInfo as x JOIN FixtureInfo as y ON x.MatchId = y.Id ORDER BY x.CreateDate DESC"""
                    cursor.execute(query)
                    observedPlayers = cursor.fetchall()
                    connection.commit()
                    return render_template('scouting.html',observedPlayers=observedPlayers)

                else:
                    deletes = request.form.getlist('scouting_to_delete')

                    for delete in deletes:
                        query = "DELETE FROM ObservedPlayerInfo WHERE ID='%d'" % int(delete)
                        cursor.execute(query)

                    return redirect(url_for('site.scouting_page'))
        else:
            return render_template('error.html')


Prim Bilgisi
-------------------------

- Prim bilgisi tablosu
   Bu tabloda futbolcuların primleri ile ilgili bilgiler yer almakta ve prim tipi(TypeID) dış anahtarı ile parametreler tablosuna başvuru yapıp parametre tablosunda var olan prim tiplerini kullanabiliriz. Ayrıca, prim bilgisinin sahibini (UserID) dış anahtarı ile kullanıcı bilgisi tablosuna başvuru yapıp prim bilgisinin hangi futbolcuya ait olduğu bilgisine ulaşabiliriz.

   Prim bilgisi daha önce olmayan futbolculara prim bilgisi eklenirken mevcut prim bilgisi olan futbolcuların prim bilgisi güncellenir. Prim bilgisi futbolcunun kontratında yer alan prim değerleri ve futbolcunun istatistik verilerine göre hesaplanır.

- Prim bilgisi ekleme/güncelleme

.. code-block:: python


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
                            if m[1] == i[0]:  #
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



- Prim bilgisi silme

.. code-block:: python

    def premiums_page():
        if current_user.userType == 'admin':
            if request.method == 'GET':
                premiums = PremiumDatabase.getPremiums()

                return render_template('premiums.html', premiums = premiums)
            else:

                deletes = request.form.getlist('premium_to_delete')
                for delete in deletes:
                    print("delete",delete)
                    PremiumDatabase.DeletePremium(delete)

                return redirect(url_for('site.premiums_page'))
        else:
            return render_template('error.html')


Parametre Bilgisi
-------------------------

- Parametre bilgisi tablosu
   Bu tabloda diğer tabloların kullanması gereken parametreler yer almaktadır. Bu parametreler kullanıcı tipi, pozisyon/mevki, şehir, antrenman tipi ve prim tipi parametreleri olmak üzere 5'e ayrılır. Parametre tablosuna birçok tablodan dış anahtarla başvuru yapılır. Parametreleri ekleme, silme, ve güncelleme yetkisi sadece yetkili yöneticiler de olup başlangıçta veritabanında yer alan parametrelerin silinmemesi gerekir. Ayrıca, sistemde kullanılan parametreler silinemez.

- Parametre bilgisi ekleme

.. code-block:: python

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

- Parametre bilgisi güncelleme

.. code-block:: python

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

- Parametre bilgisi silme

.. code-block:: python

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