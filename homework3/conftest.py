import pytest
from api.client import ApiClient


@pytest.mark.api
@pytest.fixture(scope='function')
def api_client():
    user = 'ogresresog@gmail.com'
    password = 'rTmLX43ndm'
    return ApiClient(user, password)
