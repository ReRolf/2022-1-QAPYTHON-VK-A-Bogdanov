import allure
import pytest


@allure.feature('Тесты на API')
class TestAPI:

    @pytest.mark.API
    def test_add_user(self, login_api, fake_api, mysql_builder):
        login_api.post_add_user(username=fake_api['username'],
                                password=fake_api['password'],
                                email=fake_api['email'])
        assert mysql_builder.select_by_username(fake_api['username']).username == fake_api['username']

    @pytest.mark.API
    def test_add_existent_user(self, login_api, fake_data):
        login_api.post_add_user(username=fake_data['username'], password=fake_data['password'],
                                email=fake_data['email'], expected_status=304)

    @pytest.mark.API
    def test_add_invalid_user(self, login_api, fake_api, mysql_builder):
        login_api.post_add_user(username=fake_api['username'][:3], password=fake_api['password'][:3],
                                email=fake_api['email'][:3], expected_status=400)
        assert mysql_builder.select_by_username(fake_api['username'][:3]) is None

    @pytest.mark.API
    def test_add_user_without_email(self, login_api, fake_api, mysql_client):
        login_api.post_add_user(username=fake_api['username'], password=fake_api['password'],
                                email=None, expected_status=400)
        assert mysql_client.select_by_username(fake_api['username']) is None

    @pytest.mark.API
    def test_delete_user(self, login_api, fake_api, mysql_builder, mysql_client):
        mysql_builder.add_user(username=fake_api['username'],
                               password=fake_api['password'],
                               email=fake_api['email'])
        login_api.get_delete_user(username=fake_api['username'])
        assert mysql_client.select_by_username(fake_api['username']) is None

    @pytest.mark.API
    def test_delete_not_existent_user(self, login_api):
        login_api.get_delete_user(username='BIBABOBA', expected_status=404)

    @pytest.mark.API
    def test_block_user(self, login_api, fake_api, mysql_builder, mysql_client):
        mysql_builder.add_user(username=fake_api['username'],
                               password=fake_api['password'],
                               email=fake_api['email'])
        login_api.get_block_user(username=fake_api['username'])
        assert mysql_client.select_by_username(fake_api['username']).access == 0

    @pytest.mark.API
    def test_block_not_existent_user(self, login_api, fake_api):
        login_api.get_block_user(username=fake_api['username'], expected_status=404)

    @pytest.mark.API
    def test_block_already_blocked_user(self, login_api, fake_api, mysql_builder):
        mysql_builder.add_user(username=fake_api['username'],
                               password=fake_api['password'],
                               email=fake_api['email'],
                               access=0)
        login_api.get_block_user(username=fake_api['username'], expected_status=304)

    @pytest.mark.API
    def test_unblock_user(self, login_api, fake_api, mysql_builder, mysql_client):
        mysql_builder.add_user(username=fake_api['username'], password=fake_api['password'],
                               email=fake_api['email'], access=0)
        login_api.get_unblock_user(username=fake_api['username'])
        assert mysql_client.select_by_username(fake_api['username']).access == 1

    @pytest.mark.API
    def test_unblock_not_existent_user(self, login_api, fake_api):
        login_api.get_unblock_user(username=fake_api['username'], expected_status=404)

    @pytest.mark.API
    def test_unblock_unblocked_user(self, login_api, fake_api, mysql_builder):
        mysql_builder.add_user(username=fake_api['username'],
                               password=fake_api['password'],
                               email=fake_api['email'])
        login_api.get_unblock_user(username=fake_api['username'], expected_status=304)

    @pytest.mark.API
    def test_login_not_existent_user(self, api_client):
        api_client.post_login(username='ANDREW_BOOOOOGDANOV', password='123', expected_status=401)

    @pytest.mark.API
    def test_login_without_password(self, api_client, fake_api, mysql_client):
        api_client.post_login(username=fake_api['username'], password=None, expected_status=400)

    @pytest.mark.API
    def test_find_me_error(self, login_api):
        login_api._request(method='GET', location='/static/scripts/findMeError.js',
                           expected_status=200)

    @pytest.mark.API
    def test_myapp_status(self, api_client):
        response = api_client.get_status().json()
        assert response['status'] == 'ok'
