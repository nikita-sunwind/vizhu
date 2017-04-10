'''Utility functions for test suit
'''

import time
from multidict import MultiDict
from requests import exceptions, get
import src.settings as settings


SERVER_URL = 'http://localhost:{}'.format(settings.SERVER_PORT)
EVENTS_URL = '/events'
RESTART_URL = '/restart'

BAD_DATA = r'#!,;{}[]. \n""\'/'
CONTENT_TYPE = {'Content-Type': 'application/json'}


def wait_for_server(url):
    '''Simple function for waiting for HTTP API server readiness
    '''
    for _ in range(100):
        try:
            get(url)
        except exceptions.ConnectionError:
            print('Server at {} is not ready, sleeping for 1 second...'.format(
                url))
            time.sleep(1)
        else:
            break

    print('Server at {} is ready'.format(url))


def unzip_test_cases(test_cases):
    '''Unzip test cases into two lists: test IDs and argvalues
    '''
    ids = [test_case[0] for test_case in test_cases]
    argvalues = [test_case[1:] for test_case in test_cases]

    return (ids, argvalues)


def params_to_multidict(params):
    '''Convert params to MultiDict
    '''
    multi_params = MultiDict()
    for key, value in params.items():
        if isinstance(params[key], list):
            for value in params[key]:
                multi_params.add(key, value)
        else:
            multi_params.add(key, value)

    return multi_params
