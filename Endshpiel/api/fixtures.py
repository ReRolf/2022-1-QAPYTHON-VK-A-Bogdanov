import pytest
import faker
from api.client import ApiClient


@pytest.fixture(scope='function')
def api_client(config):
    return ApiClient(base_url='http://myapp:9999/')


@pytest.fixture(scope='function')
def login_api(fake_data, api_client, mysql_builder):
    mysql_builder.add_user(username=fake_data['username'],
                           password=fake_data['password'],
                           email=fake_data['email'])
    api_client.post_login(username=fake_data['username'],
                          password=fake_data['password'])

    return api_client


@pytest.fixture(scope='function')
def fake_api():

    fake = faker.Faker()

    while True:
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        if 5 < len(username) < 17 and 10 < len(email) < 65 and len(password) < 256:
            break

    return {
        'username': username,
        'email': email,
        'password': password
    }
