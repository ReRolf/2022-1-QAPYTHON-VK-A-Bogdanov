import allure
import pytest
import requests
from faker import Faker

from app_torture import base


class TestApiCodes(base.BaseCase):
    @pytest.mark.API
    def test_status(self, setup):
        with allure.step("Checking status"):
            response = self.client.check_status()
            assert response.status_code == 200
            assert response.json().get("status") == "ok"

    @pytest.mark.API
    def test_unauthorized(self, setup):
        with allure.step("Adding user without auth"):
            response = requests.post(url=f"{pytest.url}/login", json=self.fake_user())
            assert response.status_code == 401

    @pytest.mark.API
    @pytest.mark.parametrize("bool", [True, False])
    def test_add_user(self, bool, setup, mysql_delete):
        with allure.step("Adding user and checking response"):
            response = self.client.post_user(self.fake_user(random=bool, valid=bool))
            assert response.json().get("detail") == "User added", \
                f"ResponseError: Expected '201', Got '{response.status_code}'"
            assert response.json().get("status") == "success"
            assert response.status_code == 201, f"ResponseError: Expected '201', Got '{response.status_code}'"

    @pytest.mark.API
    def test_read_user(self, setup, mysql_delete):
        with allure.step("Adding user"):
            self.client.post_user(self.fake_user())
        with allure.step("Readding user"):
            response = self.client.post_user(self.user_data)
            assert response.json().get("detail") == "User already exists"
            assert response.status_code == 304, f"ResponseError: Expected '304', Got '{response.status_code}'"

    @pytest.mark.API
    def test_none_user(self, setup):
        with allure.step("Trying to delete non existent user"):
            response = self.client.delete_user(username=self.fake_user()["username"])
            assert response.json().get("detail") == "User does not exist!"
            assert response.status_code == 404

    @pytest.mark.API
    def test_delete_user(self, setup):
        with allure.step("Adding user"):
            self.client.post_user(self.fake_user())
        with allure.step("Deleting user, checking response"):
            response = self.client.delete_user(username=self.user_data["username"])
            assert response.status_code == 204
            assert response.text != ""

    @pytest.mark.API
    def test_invalid_email(self, setup, mysql_delete):
        with allure.step("Register user with invalid email"):
            data = self.fake_user()
            data["email"] = self.fake_data(max=64)
            response = self.client.post_user(user_data=data)
            assert response.status_code == 400, f"ResponseError: Expected:400, Got:{response.status_code}"


class TestApiDatabase(base.BaseCase):

    @pytest.mark.API
    @pytest.mark.parametrize("midname, random, valid",
                             [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)])
    def test_db_check(self, midname, random, valid, setup, mysql_delete):
        with allure.step(
                f"Addnig user, checking db: "
                f"midlle_name:{bool(midname)}, data_random:{bool(random)}, data_valid:{bool(valid)}"):
            self.client.post_user(user_data=self.fake_user(midname=midname, random=random, valid=valid))
            table = self.get_row(username=self.user_data["username"])

            assert table is not None, "No such user in database"
            assert table["name"] == self.user_data[
                "name"], f"TableNameError: Expected:{self.user_data['name']}, Got:{table['name']}"
            assert table["surname"] == self.user_data[
                "surname"], f"InvalidSurnameError: Expected:{self.user_data['surname']}, Got:{table['surname']}"
            assert table["middle_name"] == self.user_data[
                "middle_name"], f"InvalidMidnameError: Expected:{self.user_data['middle_name']}, Got:{table['middle_name']}"
            assert table["password"] == self.user_data[
                "password"], f"InvalidPasswordError: Expected:{self.user_data['password']}, Got:{table['password']}"
            assert table["email"] == self.user_data[
                "email"], f"InvalidEmailError: Expected:{self.user_data['email']}, Got:{table['email']}"
            assert table["access"] == 1, f"InvalidAccessError: Expected:1, Got: {table['access']}"

    @pytest.mark.API
    def test_delete_check(self, setup):
        with allure.step("Adding user, checking database"):
            self.client.post_user(user_data=self.fake_user())
            assert self.get_row(username=self.user_data["username"]) is not None
        with allure.step("Deleting user, checking database"):
            self.client.delete_user(username=self.user_data["username"])
            assert self.get_row(username=self.user_data["username"]) is None

    @pytest.mark.API
    @pytest.mark.parametrize("max, status_code", [(0, 400), (1, 204), (255, 204), (256, 400)])
    def test_change_password_api(self, max, status_code, setup, mysql_delete):
        with allure.step(f"Adding user"):
            self.client.post_user(user_data=self.fake_user())
        with allure.step(f"Changing password, checking responce. pass_len:{max}, expect_resp:{status_code}"):
            self.user_data["password"] = self.fake_data(max=max)
            response = self.client.change_password(username=self.user_data["username"], data=self.user_data)
            assert response.status_code == status_code, f"ResponseError: Expected:{status_code}, Got:{response.status_code}"

    @pytest.mark.API
    @pytest.mark.parametrize("max", [0, 1, 2, 100, 254, 256])
    def test_change_password_db(self, max, setup, mysql_delete):
        with allure.step("Adding user"):
            self.client.post_user(user_data=self.fake_user())
            old_pass = self.get_row(self.user_data["username"])["password"]
        with allure.step("Changing password, checking database"):
            self.user_data["password"] = self.fake_data(max=max)
            self.client.change_password(username=self.user_data["username"], data=self.user_data)
            new_pass = self.get_row(self.user_data["username"])["password"]
            assert self.user_data[
                       "password"] == new_pass, f"InvalidPasswordError: Expected:{self.user_data['password']}, Got:{new_pass}"
            assert old_pass != new_pass
            assert new_pass is not None, f"Invalid len for password:{new_pass}"

    @pytest.mark.API
    def test_user_invalid_email(self, setup, mysql_delete):
        with allure.step("Add user with invalid email"):
            data = self.fake_user()
            data["email"] = self.fake_data(max=64)
            self.client.post_user(user_data=data)
            assert self.get_row(
                username=data["username"]) is None, f"Added user:{data['username']} with invalid email: {data['email']}"

    @pytest.mark.API
    def test_password_equal(self, setup, mysql_delete):
        with allure.step("Adding user"):
            self.client.post_user(user_data=self.fake_user())
        with allure.step("Changing password equal to old"):
            response = self.client.change_password(username=self.user_data["username"], data=self.user_data)
            assert response.status_code == 400
            assert response.json().get("status") == "failed"
            assert self.get_row(self.user_data["username"])["password"] == self.user_data["password"]

    @pytest.mark.API
    def test_block_user(self, setup, mysql_delete):
        with allure.step("Adding user"):
            self.client.post_user(user_data=self.fake_user())
        with allure.step("Blocking user, checking response"):
            response = self.client.block_user(username=self.user_data["username"], data=self.user_data)
            assert response.status_code == 200
            assert response.json().get("status") != "", "Response status empty"

    # Где то тут я задумался "А не добавить ли мне фикстурку добавления пользователя? Или метод". Но подумал что нет

    @pytest.mark.API
    def test_unblock_api(self, setup, mysql_delete):
        with allure.step("Adding user"):
            self.client.post_user(user_data=self.fake_user())
        with allure.step("Blocking user"):
            self.client.block_user(username=self.user_data["username"], data=self.user_data)
        with allure.step("Unblocking user via api"):
            response = self.client.unblock_user(username=self.user_data["username"], data=self.user_data)
            assert response.status_code == 200
            assert response.json().get(
                "status") != "failed", f"InvalidResponseMessage: Got:200, but msg:{response.json().get('status')}"

    @pytest.mark.API
    def test_unblock_user(self, setup, mysql_delete):
        with allure.step("Adding user"):
            self.client.post_user(user_data=self.fake_user())
        with allure.step("Blocking user"):
            self.client.block_user(username=self.user_data["username"], data=self.user_data)
        with allure.step("Unblocking user via API, checking database"):
            self.client.unblock_user(username=self.user_data["username"], data=self.user_data)
            assert self.get_row(username=self.user_data["username"])["access"] == 1

    @pytest.mark.API
    @pytest.mark.parametrize("key, max", [("name", 0), ("name", 256),
                                          ("surname", 0), ("surname", 256),
                                          ("middle_name", 256),
                                          ("username", 0), ("username", 17),
                                          ("email", 0), ("email", 65),
                                          ("password", 0), ("password", 256)])
    def test_user_invalid_key(self, key, max, setup, mysql_delete):
        with allure.step(f"Add user with field:{key}  invalid len:{max}. Check response and database"):
            data = self.fake_user()
            data[key] = self.fake_data(max=max)
            response = self.client.post_user(user_data=data)
            assert response.status_code == 400, f"ResponseError: Expected:400, Got:{response.status_code}"
            assert self.get_row(username=self.user_data[
                "username"]) is None, f"Created user {data['username']} with invalid {key}:{data[key]}"

    @pytest.mark.API
    @pytest.mark.parametrize("key, max", [("name", 1), ("name", 12), ("name", 64),
                                          ("surname", 1), ("surname", 254),
                                          ("middle_name", 0), ("middle_name", 1), ("middle_name", 254),
                                          ("username", 1), ("username", 8), ("username", 10), ("username", 15),
                                          ("username", 16),
                                          ("email", 6), ("email", 7), ("email", 36), ("email", 63), ("email", 64),
                                          ("password", 1), ("password", 255)])
    def test_user_valid_key(self, key, max, setup, mysql_delete):
        with allure.step(f"Add user with field:{key} valid len:{max}. Check response and database"):
            data = self.fake_user()
            data[key] = self.fake_data(max=max)
            response = self.client.post_user(user_data=data)
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, f"No such user:{self.user_data['username']} in database"
            assert table[key] == data[key]
            assert response.status_code == 201, f"ResponseError: Expected:201, Got:{response.status_code}"


class TestRegUser(base.BaseCase):

    @pytest.mark.API
    @pytest.mark.parametrize("midname", [True, False])
    def test_add_redirect(self, midname, setup, mysql_delete):
        with allure.step("Adding user. Checking response and redirect"):
            response = self.client.reg_user(data=self.fake_user(midname=midname))
            assert response.status_code == 200, f"ResponseError: Expected:200, Got:{response.status_code}"
            assert response.url == self.client.welcome_url, f"RedirectError: Expected:{response.url}, Got:{self.client.welcome_url}"

    @pytest.mark.API
    @pytest.mark.parametrize("middle_name", [True, False])
    def test_add_user(self, middle_name, setup, mysql_delete):
        with allure.step("Adding user. Checking database"):
            self.client.reg_user(data=self.fake_user(midname=middle_name))
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, "No such user in database"
            assert table["name"] == self.user_data[
                "name"], f"NameError: Expected:{self.user_data['name']}, Got: {table['name']}"
            assert table["surname"] == self.user_data[
                "surname"], f"SurnameError: Expected:{self.user_data['surname']}, Got: {table['surname']}"
            assert table["middle_name"] == self.user_data[
                "middle_name"], f"MidnameError: Expected:{self.user_data['middle_name']}, Got: {table['middle_name']}"
            assert table["password"] == self.user_data[
                "password"], f"PasswordError: {self.user_data['password']}, Got: {table['password']}"
            assert table["email"] == self.user_data[
                "email"], f"EmailError: Expected:{self.user_data['email']}, Got: {table['email']}"
            assert table["access"] == 1, f"AccessValueError: Expected:1, Got: {table['access']}"

    @pytest.mark.API
    @pytest.mark.parametrize("key, max", [("name", 0), ("name", 256),
                                          ("surname", 0), ("surname", 256),
                                          ("middle_name", 256),
                                          ("username", 0), ("username", 17),
                                          ("email", 0), ("email", 65),
                                          ("password", 0), ("password", 256)])
    def test_reg_user_invalid(self, key, max, setup, mysql_delete):
        with allure.step(f"Add user with field:{key}  invalid len:{max}. Check response and database"):
            data = self.fake_user()
            data[key] = self.fake_data(max=max)
            response = self.client.reg_user(data=data)
            self.client.reg_user(data=data)
            row = self.get_row(username=self.user_data["username"])
            assert response.status_code == 400, f"ResponseError: Expected:400, Got:{response.status_code}"
            assert row is None, f"Created user {row['username']} with invalid {key}:{row[key]}"

    @pytest.mark.API
    @pytest.mark.parametrize("key, max", [("name", 1), ("name", 12), ("name", 64),
                                          ("surname", 1), ("surname", 254),
                                          ("middle_name", 0), ("middle_name", 1), ("middle_name", 254),
                                          ("username", 1), ("username", 8), ("username", 10), ("username", 15),
                                          ("username", 16),
                                          ("email", 6), ("email", 7), ("email", 36), ("email", 63), ("email", 64),
                                          ("password", 1), ("password", 255)])
    def test_reg_user_valid(self, key, max, setup, mysql_delete):
        with allure.step(f"Add user with field:{key}  valid len:{max}. Check response and database"):
            data = self.fake_user()
            if key == "email":
                data[key] = self.fake_data(max=max, email=True)
            else:
                data[key] = self.fake_data(max=max)
            response = self.client.reg_user(data=data)

            assert response.status_code == 200, f"ResponseError: Expected:201, Got:{response.status_code}"
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, f"No such user:{self.user_data['username']} in database"
            assert table[key] == data[key]


class TestMockApi(base.BaseCase):

    @pytest.mark.API
    def test_mock_add_delete(self):
        with allure.step(f"Add user to mock database. Checking response"):
            self.fake_user(ui=True, valid=True)
            response = self.client.post_user_mock(username=self.user_data["username"],
                                                  id=Faker().random_int(min=0, max=99999))
            assert response.status_code == 200
        with allure.step(f"Getting list all users from mock. Checking response and added user"):
            response = self.client.get_all_users_mock()
            assert response.status_code == 200
            assert self.user_data["username"] in response.json()
        with allure.step(f"Deleting user from mock. Checking responce"):
            response = self.client.mock_delete(username=self.user_data["username"])
            assert response.status_code == 200
        with allure.step(f"Getting list all users from mock. Checking response and deleted user"):
            users = self.client.get_all_users_mock().json()
            assert self.user_data["username"] not in users

    @pytest.mark.API
    def test_get_user(self, setup, mock_add):
        with allure.step(f"Getting existed user from mock. Checking response"):
            response = self.client.get_user_mock(username=setup["username"])
            assert response.status_code == 200
            assert response.headers.get("Content-Type") == "application/json"
            assert response.json().get("vk_id") == self.vk_id
        with allure.step(f"Trying to get non existent user from mock. Checking responce"):
            response = self.client.get_user_mock(username=self.fake_data(max=30))
            assert response.status_code == 404
            assert response.headers.get("Content-Type") == "application/json"
            assert response.json() == {}


class TestLoginApi(base.BaseCase):

    @pytest.mark.API
    def test_login_negative(self):
        with allure.step(f"Auth invalid creds. Expecting 401"):
            data = {
                "username": self.fake_data(min=6, max=16),
                "password": self.fake_data(min=1, max=255),
                "submit": "Login"
            }
            response = requests.post(url=f"{pytest.url}/login", json=data)
            assert response.status_code == 401


class TestAccessApi(base.BaseCase):

    @pytest.mark.API
    def test_access(self, setup):
        with allure.step(f"Getting user info, checking access not = 1"):
            user_access = self.get_row(username=setup["username"])["access"]
            assert user_access != 1
        with allure.step(f"GET main page, expect 401 and url diff"):
            response = self.client.get_main_page()
            assert response.status_code == 401
            assert response.url != self.client.welcome_url

    @pytest.mark.API
    def test_access_diff(self, setup):
        with allure.step(f"Change access = 1 to user"):
            self.mysql_update(user=setup["username"], field="access", value=1)
            assert self.get_row(username=setup["username"])["access"] == 1
        with allure.step(f"GET on main page expect 200 and valid url"):
            response = self.client.get_main_page()
            assert response.status_code == 200
            assert response.url == self.client.welcome_url
        with allure.step(f"Change access = 0 to user"):
            self.mysql_update(user=setup["username"], field="access", value=0)
            assert self.get_row(username=setup["username"])["access"] == 0
        with allure.step(f"GET on main page. Expect 401 and invalid url"):
            response = self.client.get_main_page()
            assert response.url != self.client.welcome_url
            assert response.history[0].status_code == 401
