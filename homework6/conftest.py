import pytest
from mysql.client import MySQLClient
import os


def pytest_addoption(parser):
    parser.addoption(
        "--top", action='store', default='10', help='write the number of top requests you want to add in database'
    )
    parser.addoption(
        "--user", action='store', default='5', help='write the number of user requests you want to add in database'
    )


# @pytest.fixture(scope='session')
# def top(request):
#     return request.config.getoption("--top")
#
#
# @pytest.fixture(scope='session')
# def user(request):
#     return request.config.getoption("--user")


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MySQLClient(user='root', password='pass', db_name='TEST_SQL', host='127.0.0.1', port=3306)
    mysql_client.create_db()
    mysql_client.connect()
    mysql_client.create_table('requests_amount', 'requests_top', 'requests_type', 'requests_400', 'requests_500')
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def log_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'access.log'))
