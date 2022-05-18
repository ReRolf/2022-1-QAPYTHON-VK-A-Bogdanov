import json
import threading

import requests
from flask import Flask, jsonify, request

import settings

app_data = {}

app = Flask(__name__)


@app.route('/create_user', methods=['POST'])
def create_user():
    name = json.loads(request.data)['name']
    job = json.loads(request.data)['job']

    if not app_data.get(name):
        app_data[name] = job
        data = {'name': name, 'job': job}
        return jsonify(data), 200
    else:
        return jsonify(f'User {name} already exists'), 400


@app.route('/get_job/<name>', methods=['GET'])
def get_user_job(name):
    if job := app_data.get(name):
        data = {'name': name, 'job': job}
        return jsonify(data), 200
    else:
        return jsonify(f'User {name} does not exist'), 404


@app.route('/change_job', methods=['PUT'])
def change_user_job():
    name = json.loads(request.data)['name']
    if app_data.get(name):
        new_job = json.loads(request.data)['new_job']
        app_data[name] = new_job
        data = {'name': name, 'job': new_job}
        return jsonify(data), 200
    else:
        return jsonify(f'User {name} does not exist'), 404


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    name = json.loads(request.data)['name']
    if app_data.get(name):
        app_data.pop(name)
        return jsonify(f'You killed {name} '), 200
    else:
        return jsonify(f'User {name} does not exist'), 404


# @app.route('/shutdown')
# def mock_shutdown():
#     terminate_server = request.environ.get('werkzeug.server.shutdown')
#     if terminate_server:
#         terminate_server()
#     return jsonify(f'sudo shutdown -h 0'), 200

def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    server.start()
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}')
    return server
