from models.models import RequestsAmount, RequestsTop, RequestsType, Requests400, Requests500


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_requests_amount(self, count):
        data = RequestsAmount(count=count)
        self.client.session.add(data)
        return data

    def create_requests_type(self, request_type, count):
        data = RequestsType(request_type=request_type, count=count)
        self.client.session.add(data)
        return data

    def create_requests_top(self, url, count):
        data = RequestsTop(url=url, count=count)
        self.client.session.add(data)
        return data

    def create_requests_400(self, url, size, ip):
        data = Requests400(url=url, size=size, ip=ip)
        self.client.session.add(data)
        return data

    def create_requests_500(self, ip, requests_number):
        data = Requests500(ip=ip, requests_number=requests_number)
        self.client.session.add(data)
        return data