from datetime import datetime

import allure
import docker
import pytest
from faker import Faker
from pytest import FixtureRequest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from api.client import ApiClient
from mysql.client import MysqlClient

fake = Faker()


class BaseCase:
    auth = None
    user_data = None
    browser = None
    vk_id = None
    mysql_client = MysqlClient(db_name='vkeducation', user='root', password='pass')
    client = ApiClient()
    docker_client = docker.from_env()
    url = pytest.url

    @pytest.fixture(scope="session")
    def setup(self):
        with allure.step("Add user to auth db"):
            self.mysql_client.connect()
            self.mysql_client.insert(user_data=self.fake_user(auth=True, ui=True))
        with allure.step("Added user auth. Chech response and url"):
            response = self.client.auth(user_data=self.auth)
            assert response.status_code == 200
            assert response.url == f"{pytest.url}/welcome/"
        yield self.auth
        with allure.step("Delete added user"):
            self.mysql_client.connect()
            self.mysql_client.delete(username=self.auth["username"])
            self.mysql_client.connection.close()

    @pytest.fixture(scope="function")
    def browser(self, request):
        selenoid = request.config.getoption('--selenoid')
        if selenoid:
            pytest.url_ui = "http://app:9999"
            options = webdriver.ChromeOptions()
            self.browser = webdriver.Remote("http://localhost:4444/wd/hub", options=options)
        else:
            self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.browser.maximize_window()
        failed_tests_count = request.session.testsfailed
        yield
        pytest.url_ui = "http://127.0.0.1:9999"
        if request.session.testsfailed > failed_tests_count:
            self.browser.get_screenshot_as_file(f"log/ui/screenshot/{request.node.name}.png")
            with open(f"log/ui/logs/{request.node.name}.log", "w") as file:
                for i in self.browser.get_log("browser"):
                    file.write(f"{i['level']} - {i['source']}\n\n{i['message']}\n\n")
            allure.attach.file(f"log/ui/screenshot/{request.node.name}.png", "fail.png", allure.attachment_type.PNG)
            with open(f"log/ui/logs/{request.node.name}.log", 'r') as file:
                allure.attach(file.read(), 'browser.log', allure.attachment_type.TEXT)
        self.browser.quit()

    @pytest.fixture(scope="function")
    def mysql_delete(self):
        yield
        self.mysql_client.connect()
        self.mysql_client.delete(username=self.user_data["username"])

    def mysql_update(self, field: str, value, user: str):
        self.mysql_client.update(username=user, user_data={field: value})

    @pytest.fixture(scope="function")
    def mock_add(self, setup):
        self.vk_id = fake.random_int(min=0, max=99999)
        response = self.client.post_user_mock(username=setup["username"], id=self.vk_id)
        yield response
        self.client.mock_delete(username=setup["username"])

    def fake_data(self, max, min=None, email=False, random=False):
        if not min:
            min = max
        if random:
            min = 1
        if email:
            return fake.pystr(max_chars=max - 10, min_chars=min - 10) + '@gmail.com'
        return fake.pystr(max_chars=max, min_chars=min)

    def fake_ui(self, key, max, valid=False):
        self.fake_user(ui=True, random=False, valid=valid)
        if key == "email":
            self.user_data[key] = self.fake_data(max=max, email=True)
        elif key == "password":
            self.user_data[key] = self.fake_data(max=max)
            self.user_data["password_confirm"] = self.user_data[key]
        else:
            self.user_data[key] = self.fake_data(max=max, random=False)
        return self.user_data

    def fake_user(self, midname=True, random=False, valid=True, auth=False, ui=False) -> dict:
        user_data = {
            "name": self.fake_data(min=1, max=45, random=random),
            "surname": self.fake_data(min=1, max=300, random=random),
            "middle_name": self.fake_data(max=300, random=random) if midname else None,
            "username": self.fake_data(min=6, max=16, random=random),
            "email": self.fake_data(min=6, max=64, email=True, random=random),
            "password": self.fake_data(min=6, max=255, random=random),
        }
        if valid:
            user_data["middle_name"] = self.fake_data(max=255, random=random) if midname else None
            user_data["surname"] = self.fake_data(min=1, max=255, random=random)
            user_data["email"] = self.fake_data(min=6, max=64, email=True, random=random)
        if ui:
            user_data["surname"] = self.fake_data(min=1, max=255, random=random)
            user_data["middle_name"] = self.fake_data(max=255, random=random) if midname else None
            if valid:
                user_data = {
                    "name": self.fake_data(min=1, max=20, random=random),
                    "surname": self.fake_data(min=1, max=20, random=random),
                    "middle_name": self.fake_data(max=20, random=random) if midname else None,
                    "username": self.fake_data(min=6, max=16, random=random),
                    "email": self.fake_data(min=6, max=64, email=True, random=random),
                    "password": self.fake_data(min=6, max=50, random=random),
                }
        if auth:
            self.auth = user_data
        else:
            self.user_data = user_data

        return user_data

    def get_row(self, username):
        try:
            return self.mysql_client.get_row(username)[0]
        except IndexError:
            return None

    @pytest.fixture(scope="function", autouse=True)
    def report(self, request: FixtureRequest):
        failed_tests_count = request.session.testsfailed
        start = datetime.now()
        app_container = self.docker_client.containers.list(filters={"name": "app"})[0]
        yield
        if request.session.testsfailed > failed_tests_count:
            with open(f"log/api/logs/app_logs_{request.node.name}.log", "w") as file:
                for line in app_container.logs(stream=True, since=start, until=datetime.now(), follow=False):
                    file.write(f'{line.decode("utf-8").strip()}\n')
            with open(f"log/api/logs/app_logs_{request.node.name}.log", 'r') as file:
                allure.attach(file.read(), 'app_log.log', allure.attachment_type.TEXT)
