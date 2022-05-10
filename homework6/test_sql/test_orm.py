import pytest

import log_parse
from models.models import RequestsAmount, RequestsTop, RequestsType, Requests400, Requests500
from mysql.client import MySQLClient
from utils.builder import MySQLBuilder


class BaseMySQL:

    def parse(self, log_path):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, log_path):
        self.client: MySQLClient = mysql_client
        self.builder: MySQLBuilder = MySQLBuilder(self.client)
        self.parse(log_path)


class TestRequestsAmount(BaseMySQL):

    def parse(self, log_path):
        data = log_parse.get_requests_amount(log_path)
        self.builder.create_requests_amount(data)

    def test_requests_amount(self):
        assert len(self.client.session.query(RequestsAmount).all()) == 1


class TestRequestsTop(BaseMySQL):

    def parse(self, log_path):
        data = log_parse.get_requests_top(log_path)
        for _ in data:
            self.builder.create_requests_top(url=_[0], count=_[1])
        self.result = len(data)

    def test_requests_top(self):
        data = self.client.session.query(RequestsTop).all()
        assert len(data) == self.result


class TestRequestType(BaseMySQL):

    def parse(self, log_path):
        data = log_parse.get_requests_type(log_path)
        for _ in data:
            self.builder.create_requests_type(request_type=_[0], count=_[1])
        self.result = len(data)

    def test_request_type(self):
        data = self.client.session.query(RequestsType).all()
        assert len(data) == self.result


class TestRequests400(BaseMySQL):

    def parse(self, log_path):
        data = log_parse.get_requests_400(log_path)
        for _ in data:
            self.builder.create_requests_400(url=_[0], size=_[1], ip=_[2])
        self.result = len(data)

    def test_requests_400(self):
        data = self.client.session.query(Requests400).all()
        assert len(data) == self.result


class TestRequests500(BaseMySQL):

    def parse(self, log_path):
        data = log_parse.get_requests_500(log_path)
        for _ in data:
            self.builder.create_requests_500(ip=_[0], requests_number=_[1])
        self.result = len(data)

    def test_requests_500(self):
        data = self.client.session.query(Requests500).all()
        assert len(data) == self.result
