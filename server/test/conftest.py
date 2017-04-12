# pylint: disable=redefined-outer-name

'''Pytest fixture definitions
'''

from pytest import fixture
from src.server import create_app
from test.utils import N_TEST_EVENTS, generate_events


@fixture
def fx_client(loop, test_client):
    '''Create test client
    '''
    return loop.run_until_complete(test_client(create_app))


@fixture
def fx_load_fixtures(fx_client):
    '''Load fixture data into the database
    '''
    session = fx_client.server.app['Session']()
    generate_events(session, N_TEST_EVENTS)
