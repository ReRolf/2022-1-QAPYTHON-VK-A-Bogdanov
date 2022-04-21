import os
import sys
import shutil
import logging

from base import BaseCase
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--selenoid', action='store_true')
@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def credentials(repo_root):
    with open(os.path.join(repo_root, 'user_data', 'logpass.txt'), 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password


@pytest.fixture(scope='session')
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def logger(base_temp_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(base_temp_dir, 'test.log')
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    log_level = logging.INFO
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

@pytest.fixture(scope='session')
def config(request):
    if request.config.getoption('--selenoid'):
        selenoid = 'http://127.0.0.1:4444/wd/hub'
    else:
        selenoid = None
    return {'selenoid': selenoid}

