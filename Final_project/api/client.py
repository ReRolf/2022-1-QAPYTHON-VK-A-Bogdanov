import allure
import requests
from urllib.parse import urljoin


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    @allure.step('Отправление {method} запроса по URL: {location}. Ожидаемый статус: {expected_status}')
    def _request(self, method, location, expected_status=200, headers=None, json=None, data=None):
        url = urljoin(self.base_url, location)

        response = self.session.request(method, url, headers=headers, json=json, data=data)

        if response.status_code != expected_status:
            if method == 'POST':
                allure.attach(name='POST-запрос',
                              body=f"'URL': {response.request.url}, 'Body': {response.request.body}",
                              attachment_type=allure.attachment_type.TEXT)
            elif method == 'GET':
                allure.attach(name='GET-запрос',
                              body=f'URL: {response.request.url}',
                              attachment_type=allure.attachment_type.TEXT)

            allure.attach(name='RESPONSE',
                          body=f"'Body': {response.text}, 'Status_code': {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

            raise ResponseStatusCodeException(f'Получено {response.status_code} {response.reason} для URL: {url}! '
                                              f'Ожидаемый код ответа: {expected_status}.')

        return response

    @allure.step('Авторизация пользователя {username} через API')
    def post_login(self, username, password, expected_status=200):
        location = '/login'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        if username and password:
            data = {
                'username': username,
                'password': password,
                'submit': 'Login'
            }
        elif password is None:
            data = {
                'username': username,
                'submit': 'Login'
            }

        response = self._request('POST', location, headers=headers, data=data, expected_status=expected_status)

        return response

    @allure.step('Добавление пользователя {username} через API')
    def post_add_user(self, username, password, email, expected_status=201):
        location = '/api/add_user'

        headers = {
            'Content-Type': 'application/json'
        }

        if username and password and email:
            data = {
                "username": username,
                "password": password,
                "email": email
            }
        elif email is None:
            data = {
                "username": username,
                "password": password
            }

        response = self._request('POST', location, headers=headers, json=data, expected_status=expected_status)

        return response

    @allure.step('Удаление пользователя {username} через API')
    def get_delete_user(self, username, expected_status=204):
        location = f'/api/del_user/{username}'

        response = self._request('GET', location, expected_status=expected_status)

        return response

    @allure.step('Блокировка пользователя {username} через API')
    def get_block_user(self, username, expected_status=200):
        location = f'/api/block_user/{username}'

        response = self._request('GET', location, expected_status=expected_status)

        return response

    @allure.step('Разблокировка пользователя {username} через API')
    def get_unblock_user(self, username, expected_status=200):
        location = f'/api/accept_user/{username}'

        response = self._request('GET', location, expected_status=expected_status)

        return response

    @allure.step('Получение статуса приложения')
    def get_status(self, expected_status=200):
        location = '/status'

        response = self._request('GET', location, expected_status=expected_status)

        return response
