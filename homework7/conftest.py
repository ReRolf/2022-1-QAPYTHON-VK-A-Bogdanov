import pytest
from mock import flask_mock
from mock.client import MockClient
import settings


@pytest.fixture(scope='session')
def connect():
    flask_mock.run_mock()
    client = MockClient(settings.MOCK_HOST, settings.MOCK_PORT)
    yield client
    client.get('/shutdown')
