from collections import Counter
from fnmatch import fnmatch
from urllib.parse import quote_plus
import os


def log_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'access.log'))


def get_requests_amount(log_path):
    with open(log_path, 'r') as logs:
        log = len(logs.readlines())
    return log


def get_requests_type(log_path):
    with open(log_path, 'r') as logs:
        log = [_.split()[5][1:] for _ in logs.readlines()]
        log = Counter(log).most_common()
    return log


def get_requests_top(log_path):
    with open(log_path, 'r') as logs:
        log = [quote_plus(_.split()[6]) for _ in logs.readlines()]
        log = Counter(log).most_common(10)
    return log


def get_requests_400(log_path):
    with open(log_path, 'r') as logs:
        log = [
            (quote_plus(_.split()[6]), int(_.split()[8]), int(_.split()[9]), _.split()[0])
            for _ in logs.readlines() if fnmatch(_.split()[8], '4??')]
        log.sort(key=lambda req: req[2], reverse=True)
    return log[:5]


def get_requests_500(log_path):
    with open(log_path, 'r') as logs:
        log = [_.split()[0] for _ in logs.readlines() if fnmatch(_.split()[8], '5??')]
        log = Counter(log).most_common(5)
    return log
