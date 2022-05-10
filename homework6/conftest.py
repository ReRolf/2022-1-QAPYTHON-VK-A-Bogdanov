import pytest
from mysql.client import MySQLClient
import os


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MySQLClient(user='root', password='0000', db_name='TEST_SQL', host='127.0.0.1', port=3306)
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MySQLClient(user='root', password='0000', db_name='TEST_SQL', host='127.0.0.1', port=3306)
        mysql_client.create_db()
        mysql_client.connect()
        mysql_client.create_table('requests_amount', 'requests_top', 'requests_type', 'requests_400', 'requests_500')
        mysql_client.connection.close()


@pytest.fixture(scope='session')
def log_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'access.log'))
