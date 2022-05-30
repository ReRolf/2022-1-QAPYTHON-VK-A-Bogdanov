import json
from flask import Flask

users = {}

vk_id_mock = Flask(__name__)


@vk_id_mock.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    if username in users.keys():
        return json.dumps({'vk_id': users[username]}), 200
    else:
        return json.dumps({}), 404


@vk_id_mock.route('/status')
def get_status():
    return 'OK', 200


@vk_id_mock.route('/add_user/<username>', methods=['POST'])
def add_user(username):
    vk_id = len(users) + 1
    users[username] = vk_id
    return f'User {username} added. VK ID: {vk_id}.', 201


if __name__ == '__main__':
    vk_id_mock.run(host='0.0.0.0', port=9000)
