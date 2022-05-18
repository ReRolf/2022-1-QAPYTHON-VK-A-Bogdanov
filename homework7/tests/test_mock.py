import json
from base import MockBase
from mock.flask_mock import app_data
from utils.data_gen import create_name, create_job


class TestCreate(MockBase):
    def test_create_user(self, connect):
        user, response = self.create_user(connect)
        assert response['status_code'] == 200

        response = json.loads(response['response'])
        assert response['name'] == user['name']
        assert response['job'] == user['job']

    def test_recreate_user(self, connect):
        user, response = self.create_user(connect)
        assert response['status_code'] == 200

        response = connect.post('/create_user', user)
        assert response['status_code'] == 400


class TestGet(MockBase):
    def test_get_job(self, connect):
        user, response = self.create_user(connect)
        assert response['status_code'] == 200

        name = user.get('name')
        response = connect.get(f'/get_job/{name}')
        assert response['status_code'] == 200

        response = json.loads(response['response'])
        assert response['job'] == app_data[name]

    def test_get_job_noname(self, connect):
        noname = create_name() + 'noname'
        response = connect.get(f'/get_job/{noname}')
        assert response['status_code'] == 404


class TestDelete(MockBase):
    def test_delete_user(self, connect):
        user, response = self.create_user(connect)
        assert response['status_code'] == 200

        response = connect.delete('/delete_user', user)
        assert response['status_code'] == 200

    def test_delete_noname(self, connect):
        name = create_name()
        noname = {'name': f'new{name}'}
        response = connect.delete('/delete_user', noname)
        assert response['status_code'] == 404


class TestPut(MockBase):
    def test_change_job(self, connect):
        user, response = self.create_user(connect)
        assert response['status_code'] == 200

        user['new_job'] = create_job()
        response = connect.put('/change_job', user)
        assert response['status_code'] == 200

        response = json.loads(response['response'])
        assert response['job'] == user['new_job']

    def test_change_job_noname(self, connect):
        user = {'name': create_name() + create_name(), 'job': create_job(), 'new_job': create_job()}
        response = connect.put('/change_job', user)
        assert response['status_code'] == 404
