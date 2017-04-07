'''Utility functions for test suit
'''

import time
from requests import exceptions, get


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

    print('Server at {} is ready'.format(url))


def unzip_test_cases(test_cases):
    '''Unzip test cases into two lists: test IDs and argvalues
    '''
    unzipped = zip(*test_cases)
    ids = next(unzipped)
    argvalues = next(unzipped)

    return (ids, argvalues)
