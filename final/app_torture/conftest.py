import sys
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption('--selenoid', action='store_true')


def pytest_configure():
    pytest.url = "http://127.0.0.1:9999"
    pytest.url_ui = "http://127.0.0.1:9999"
    pytest.mock = "http://127.0.0.1:9000"
    if sys.platform.startswith('win'):
        base_dir = 'C:\\app_torture'
    else:
        base_dir = './log'
    Path(f'{base_dir}/api/logs').mkdir(parents=True, exist_ok=True)
    Path(f'{base_dir}/ui/logs').mkdir(parents=True, exist_ok=True)
    Path(f'{base_dir}/ui/screenshot').mkdir(parents=True, exist_ok=True)
