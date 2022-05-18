import json
import socket


class MockClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect.settimeout(20)
        connect.connect((self.host, self.port))
        return connect

    def request(self, request_type, url, data=''):
        request = f'{request_type} {url} HTTP/1.1\r\nHost: {self.host}\r\n'

        if data:
            data = json.dumps(data)
            data_type = 'Content-Type: application/json'
            data_length = 'Content-Length: ' + str(len(data))
            request += f'{data_type}\r\n{data_length}\r\n\r\n' + data
        else:
            request += f'\r\n'

        return request.encode()

    def response(self, connect):
        data = []
        while True:
            socket_data = connect.recv(1024)
            if socket_data:
                data.append(socket_data.decode())
            else:
                break
        connect.close()

        data = ''.join(data).splitlines()
        return {'status_code': int(data[0].split(' ')[1]), 'response': data[-1]}

    def get(self, url):
        connect = self.connect()
        request = self.request('GET', url)
        connect.send(request)
        return self.response(connect)

    def post(self, url, data):
        connect_post = self.connect()
        request = self.request('POST', url, data=data)
        connect_post.send(request)
        return self.response(connect_post)

    def put(self, url, data):
        connect = self.connect()
        request = self.request('PUT', url, data=data)
        connect.send(request)
        return self.response(connect)

    def delete(self, url, data):
        connect = self.connect()
        request = self.request('DELETE', url, data=data)
        connect.send(request)
        return self.response(connect)
