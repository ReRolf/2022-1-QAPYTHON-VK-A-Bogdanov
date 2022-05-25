import os
import shutil
import pytest
import faker
from mysql.builder import MySQLBuilder
from mysql.client import MySQLClient


def pytest_addoption(parser):
    parser.addoption('--url', default='http://myapp:9999')


def pytest_configure(config):
    base_test_dir = '/home/rolf/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture(scope='function')
def test_dir(request):

    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def fake_data():

    fake = faker.Faker()

    while True:
        username = fake.user_name() + fake.user_name()
        email = fake.email()
        password = fake.password()
        if 5 < len(username) < 17 and 10 < len(email) < 65 and len(password) < 256:
            break

    return {
        'username': username,
        'email': email,
        'password': password
    }


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MySQLClient()
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def mysql_builder(mysql_client):
    return MySQLBuilder(mysql_client)
