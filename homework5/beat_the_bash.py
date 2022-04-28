import os
from collections import Counter


class PythonBash:
    abs_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
    cool_line = '\n' + "─" * 75

    def __init__(self):
        self.logs = os.path.join(self.abs_path, 'access.log')
        self.results = os.path.join(self.abs_path, 'results.txt')

    def requests_amount(self):
        with open(self.logs, 'r') as logs:
            log = len(logs.readlines())
        with open(self.results, 'w') as results:
            results.writelines([self.cool_line, '\nTotal Requests:  ', str(log)])

    # def  request_type(self):
    #     with open(self.logs, 'r') as logs:
    #         log = [log.split()[5][1:] for log in logs.readlines()]
    #         result = numpy.column_stack(numpy.unique(log, return_counts=True))
    #         print(result)
    #     with open(self.results, 'w') as results:
    #         numpy.savetxt(results, result, fmt=['%s\t','%s'])

    def request_type(self):
        with open(self.logs, 'r') as logs:
            log = [log.split()[5][1:] for log in logs.readlines()]
            log = Counter(log).most_common()
        with open(self.results, 'a') as results:
            results.writelines([self.cool_line, '\nRequest amount by type:  \n'])
            results.writelines([f'{text[0]}: \t{text[1]}\n' for text in log])
            # for text in log:
            #     results.writelines(str(text))

    def top_requests(self):
        with open(self.logs, 'r') as logs:
            log = [log.split()[6] for log in logs.readlines()]
            log = Counter(log).most_common(10)
        with open(self.results, 'a') as results:
            results.writelines([self.cool_line, 'Top 10 requests:\n'])
            results.writelines([f'{text[0]}: \t{text[1]}\n' for text in log])

    def requests_400(self):
        # with open(self.logs, 'r') as logs:
        #     log = logs.readlines()
        #     log = ''.join(log)
        #     print(log)
        #     log = re.findall(r'4..', log)
        #     print(log)
        with open(self.logs, 'r') as logs:
            log = [(text.split()[6], text.split()[8], text.split()[9], text.split()[0]) for text in logs.readlines()]
            prefix = ['4']
            new_log = []
            for items in log:
                if items[1].startswith(tuple(prefix)):
                    new_log.append(items)
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
        with open(self.results, 'a') as results:
            results.writelines([self.cool_line, '\nTop 5 ip by number of requests with (5XX) error:\n', ])
            results.writelines([f'\n~ IP: {text[0]}\nRequests: {text[1]}\n\n' for text in new_log])


log_parse = PythonBash()
log_parse.requests_amount()
log_parse.request_type()
log_parse.top_requests()
log_parse.requests_400()
log_parse.top_user_ip()
