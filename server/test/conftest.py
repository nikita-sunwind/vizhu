# pylint: disable=redefined-outer-name

'''Pytest fixture definitions
'''

from json import dumps
from random import random
from time import time
from uuid import uuid4
from pytest import fixture
from src.models import Event
from src.server import create_app
from test.utils import BAD_DATA


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

    timestamp = time()
    for _ in range(1000):
        event = Event(
            _id=str(uuid4()),
            _series='demo',
            _agent='Smith',
            _timestamp=timestamp,
            _data=dumps({
                'roundtrip_delay': random(),
                'bad_data': BAD_DATA,
            }))

        session.add(event)
        timestamp += 0.1

    session.commit()
