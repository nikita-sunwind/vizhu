# pylint: disable=redefined-outer-name

'''Pytest fixture definitions
'''

import subprocess
from pytest import yield_fixture
from test.utils import SERVER_URL, wait_for_server


@yield_fixture(scope='session')
def fx_api_server():
    '''Start HTTP REST API server
    '''
    args = ['python', '-m', 'src.server']
    devnull = open('/dev/null', 'w')
    server = subprocess.Popen(args, stdout=devnull)
    wait_for_server(SERVER_URL)

    yield

    # Release resources
    server.terminate()
    devnull.close()
