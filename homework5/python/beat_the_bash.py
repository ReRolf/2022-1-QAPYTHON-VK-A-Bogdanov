import os
import json
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--json', action='store_true', help='write prossesed data in .json file')
args = parser.parse_args()


class ParsingText:
    abs_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
    dir_path = os.path.join(abs_path, 'results/')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    cool_line = '\n' + "─" * 75

    def __init__(self):
        self.logs = os.path.join(self.abs_path, 'access.log')
        self.results = os.path.join(self.abs_path, 'results.txt')
        self.json_results = os.path.join(self.abs_path, 'results.json')

    def requests_amount(self):
        with open(self.logs, 'r') as logs:
            log = len(logs.readlines())
        if args.json:
            with open(os.path.join(self.dir_path, 'results_request_amount.json'), 'a') as json_file:
                json.dump({'Total_requests': str(log)}, json_file, indent=4, sort_keys=True)
        else:
            with open(self.results, 'a') as results:
                results.writelines([self.cool_line, '\nTotal Requests:  ', str(log)])

    def request_type(self):
        with open(self.logs, 'r') as logs:
            log = [log.split()[5][1:] for log in logs.readlines()]
            log = Counter(log).most_common()
        if args.json:
            with open(os.path.join(self.dir_path, 'results_request_type.json'), 'a') as json_file:
                json.dump({'Type_amount': [f'{text[0]}: {text[1]}' for text in log]}, json_file, indent=4,
                          sort_keys=True)
        else:
            with open(self.results, 'a') as results:
                results.writelines([self.cool_line, '\nRequest amount by type:  \n'])
                results.writelines([f'{text[0]}: \t{text[1]}\n' for text in log])

    def top_requests(self):
        with open(self.logs, 'r') as logs:
            log = [log.split()[6] for log in logs.readlines()]
            log = Counter(log).most_common(10)
        if args.json:
            with open(os.path.join(self.dir_path, 'results_top_requests.json'), 'a') as json_file:
                json.dump({'Top_ten_requests': [f'{text[0]}: {text[1]}' for text in log]}, json_file, indent=4,
                          sort_keys=True)
        else:
            with open(self.results, 'a') as results:
                results.writelines([self.cool_line, 'Top 10 requests:\n'])
                results.writelines([f'{text[0]}: \t{text[1]}\n' for text in log])

    def requests_400(self):
        with open(self.logs, 'r') as logs:
            log = [(text.split()[6], text.split()[8], text.split()[9], text.split()[0]) for text in logs.readlines()]
            prefix = ['4']
            new_log = []
            for items in log:
                if items[1].startswith(tuple(prefix)):
                    new_log.append(items)
        if args.json:
            with open(os.path.join(self.dir_path, 'results_requests_400.json'), 'a') as json_file:
                json.dump({'Request_400': [f'URL:{text[0]}'
                                           f'Response:{text[1]}'
                                           f'Size: {text[2]}'
                                           f'Ip:{text[3]}' for text in new_log[:5]]}, json_file, indent=4,
                          sort_keys=True)
        else:
            with open(self.results, 'a') as results:
                results.writelines([self.cool_line, '\n10 largest requests with (4XX) Error:\n'])
                results.writelines(
                    [f'\n~ URL:{text[0]}\n~ Response:{text[1]}\n~ Size: {text[2]}\n~ Ip:{text[3]}\n' for text in
                     new_log[:5]])

    def top_user_ip(self):
        with open(self.logs, 'r') as logs:
            log = [(text.split()[6], text.split()[8], text.split()[0]) for text in logs.readlines()]
            prefix = ['5']
            new_log = []
            for items in log:
                if items[1].startswith(tuple(prefix)):
                    new_log.append(items[2])
            new_log = Counter(new_log).most_common(5)
        if args.json:
            with open(os.path.join(self.dir_path, 'results_requests_500.json'), 'a') as json_file:
                json.dump({'Requests_500': [f'IP: {text[0]}'
                                            f'Requests: {text[1]}' for text in new_log]},
                          json_file, indent=4, sort_keys=True)
        else:
            with open(self.results, 'a') as results:
                results.writelines([self.cool_line, '\nTop 5 ip by number of requests with (5XX) error:\n', ])
                results.writelines([f'\n~ IP: {text[0]}\nRequests: {text[1]}\n\n' for text in new_log])


log_parse = ParsingText()
log_parse.requests_amount()
log_parse.request_type()
log_parse.top_requests()
log_parse.requests_400()
log_parse.top_user_ip()