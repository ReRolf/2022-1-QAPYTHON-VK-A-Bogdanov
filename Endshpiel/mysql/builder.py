import allure
from mysql.models import TestUser


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    @allure.step("Добавление пользователя ({username}) в DB")
    def add_user(self, username, password, email, access=1):
        test_user = TestUser(
            username=username,
            password=password,
            email=email,
            access=access
        )
        self.client.session.add(test_user)
        self.client.session.commit()
        return test_user
