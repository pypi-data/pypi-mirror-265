import pytest
from .. import src
import os
import pymssql
from sqlalchemy.pool import NullPool
import mariadb

def test_mssql_db_error():
    with pytest.raises(pymssql._pymssql.OperationalError):
        db = src.MsSQLDatabase(
            server = os.getenv('DB_mssql_SERVER'),
            port=os.getenv('DB_mssql_PORT'),
            user = os.getenv('DB_mssql_USER_ERROR'),
            password = os.getenv('DB_mssql_PASSWORD_ERROR'),
            database = os.getenv('DB_mssql_DATABASE'))
        with db as conn:
            res = conn.execute('SELECT * FROM DockerTest.dbo.Person')

def test_maria_db_error():
    with pytest.raises(mariadb.Error):
        db = src.MariaDatabase(
            server = os.getenv('DB_mariadb_SERVER'),
            user = os.getenv('DB_mariadb_USER_ERROR'),
            password = os.getenv('DB_mariadb_PASSWORD_ERROR'),
            database = os.getenv('DB_mariadb_DATABASE'))
        with db as conn:
            res = conn.execute('SELECT * FROM DockerTest.dbo.Person')
            
def test_mssql_db_success():
    db = src.MsSQLDatabase(
            server = os.getenv('DB_mssql_SERVER'),
            user = os.getenv('DB_mssql_USER'),
            password = os.getenv('DB_mssql_PASSWORD'),
            database = os.getenv('DB_mssql_DATABASE'),
            pool_size=NullPool)
    assert db.connected


def test_maria_db_success():
    db = src.MariaDatabase(
            server = os.getenv('DB_mariadb_SERVER'),
            user = os.getenv('DB_mariadb_USER'),
            password = os.getenv('DB_mariadb_PASSWORD'),
            database = os.getenv('DB_mariadb_DATABASE'),
            pool_size=NullPool)
    assert db.connected