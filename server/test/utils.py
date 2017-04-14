'''Utility functions for test suit
'''

from json import dumps
from random import random
from time import time
from uuid import uuid4
from multidict import MultiDict
from src.exports import DATABASE_PAGESIZE
from src.models import Event


EVENTS_URL = '/events'
RESTART_URL = '/restart'

BAD_DATA = r'#!,;{}[]. \n""\'/'
COMPOUND_DATA = ['a', 2, .3, None, BAD_DATA, {'b': ['c', 'd', 'e']}]
N_TEST_EVENTS = 1000


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


def generate_events(db_session, n_events):
    '''Generate random events and insert them into the database
    '''
    timestamp = time()
    for position in range(n_events):
        event = Event(
            _id=str(uuid4()),
            _series='demo',
            _agent='Smith',
            _timestamp=timestamp + random(),
            _data=dumps({
                'roundtrip_delay': random(),
                'bad_data': BAD_DATA,
                'compound_data': COMPOUND_DATA,
            }))

        db_session.add(event)
        timestamp += 0.1

        if position % DATABASE_PAGESIZE == DATABASE_PAGESIZE - 1:
            db_session.commit()

    db_session.commit()
