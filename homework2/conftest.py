import logging
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--debug_log', action='store_true')


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
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')
    if request.config.getoption('--selenoid'):
        selenoid = 'http://127.0.0.1:80/wd/hub'
    else:
        selenoid = None
    return {
        'debug_log': debug_log,
        'selenoid': selenoid,
    }


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
