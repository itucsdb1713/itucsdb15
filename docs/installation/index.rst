Kurulum Kılavuzu
================

Gerekli Programlar
------------------

**Yüklenecekler**

1- Python 3.6.x sürümü bu linkten yüklenebilir: https://www.python.org/downloads/

2- PostgreSQL bu linkten yüklenebilir: https://www.postgresql.org/download/

3- Git versiyon kontrol aracı bu linkten yüklenebilir: https://git-scm.com/downloads

4- Pgadmin bu linkten yüklenebilir:  https://www.pgadmin.org/download/

5- Flask bu linkten yüklenebilir: http://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz

Veya pip kullanılarak 'cmd' üzerinden aşağıdaki gibi yüklenebilir:

.. code-block:: python

	pip install Flask

6- Flask-Login pip kullanılarak 'cmd' üzerinden aşağıdaki gibi yüklenebilir:

.. code-block:: python

	pip install Flask-Login

7- passlib pip kullanılarak 'cmd' üzerinden aşağıdaki gibi yüklenebilir:

.. code-block:: python

	pip install passlib

8- Psycopg2 pip kullanılarak 'cmd' üzerinden aşağıdaki gibi yüklenebilir:

.. code-block:: python

	pip install psycopg2

**Projeyi Çalıştırma**

Komut satırında projenin klasörüne gidilerek "git" ile projenin kaynak kodları Github üzerinden çekilir.

- Komut satırında git versiyon kontrol sistemi ile aşağıdaki adımlar izlenerek proje çekilebilir.

.. code-block:: python

    git init
    git remote add origin https://github.com/itucsdb1713/itucsdb1713
    git pull origin master

-  pgAdmin üzerinde yeni sunucu ve veritabanı oluşturularak projenin veritabanı gözlenebilir ve SQL sorguları yapılabilir.

.. code-block:: python

   username: postgres
   password: 12345
   port: 5432

- Komut satırında projenin klasörüne gidilerek proje aşağıdaki komutla çalıştırılabilir.

.. code-block:: python

	python server.py



