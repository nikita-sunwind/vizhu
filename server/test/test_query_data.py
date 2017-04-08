# pylint: disable=no-self-use

'''Query event data from the server
'''

from time import time
from uuid import uuid4
from pytest import mark
from requests import get
from test.utils import EVENTS_URL, unzip_test_cases


@mark.usefixtures('fx_api_server')
class TestQueryData:
    '''Query event data from the server
    '''

    action_cases = [

        ('can-query-events-with-all-possible-parameters',
         {
             'format': 'numpy',
             'id': uuid4(),
             'series': 'demo',
             'agent': 'Smith',
             'since': time() - 1000,
             'till': time(),
             'columns': ['_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-events-without-parameters',
         {},
         200,
         None),

    ]

    ids, argvalues = unzip_test_cases(action_cases)

    @mark.parametrize('params,code,message', argvalues, ids=ids)
    def test_query_events(self, params, code, message):

        response = get(EVENTS_URL, params=params)

        assert response.status_code == code

        if message:
            assert response.text == message
        else:
            results = response.json()
            assert isinstance(results, list)
