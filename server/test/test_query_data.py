# pylint: disable=no-self-use

'''Query event data from the server
'''

from json import dumps
from time import time
from uuid import uuid4
from pytest import mark
from requests import get, post
from test.utils import EVENTS_URL, unzip_test_cases


@mark.usefixtures('fx_api_server')
class TestQueryData:
    '''Query event data from the server
    '''

    action_cases = [

        ('can-query-data-with-all-possible-filters',
         {
             'format': 'json',
             'id': str(uuid4()),
             'series': 'series-{}'.format(str(uuid4())),
             'agent': 'agent-{}'.format(str(uuid4())),
             'since': time() - 1000,
             'till': time() + 1000,
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-without-filters',
         {
         },
         200,
         None),

        ('can-query-data-by-id',
         {
             'id': str(uuid4()),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-series',
         {
             'series': 'series-{}'.format(str(uuid4())),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-agent',
         {
             'agent': 'agent-{}'.format(str(uuid4())),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-time-period',
         {
             'since': time() - 1000,
             'till': time() + 1000,
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-time-since',
         {
             'since': time() - 1000,
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-time-till',
         {
             'till': time() + 1000,
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-nonexistent-column',
         {
             'columns': ['_id', 'weird_column'],
         },
         200,
         None),

    ]

    ids, argvalues = unzip_test_cases(action_cases)

    @mark.parametrize('params,code,message', argvalues, ids=ids)
    def test_can_query_data(self, params, code, message):

        event_id = params.get('id', str(uuid4()))

        payload = {
            '_id': event_id,
            '_series': params.get('series', 'demo'),
            '_agent': params.get('agent', 'Smith'),
            '_timestamp': time(),
            'roundtrip_delay': 0.001,
        }

        response = post(EVENTS_URL, data=dumps(payload))
        assert response.status_code == 200

        response = get(EVENTS_URL, params=params)
        assert response.status_code == code

        if message:
            assert response.text == message
            return

        results = response.json()
        assert isinstance(results, list)

        # Our newly loaded event should be present in results
        result_ids = set(event['_id'] for event in results)
        assert event_id in result_ids

        # Server should return either all selected columns
        # or all existing columns if no one is selected
        selected_columns = set(params.get('columns', []))
        existing_columns = set(payload.keys())
        if selected_columns:
            columns = selected_columns
        else:
            columns = existing_columns

        for event in results:
            for column in columns:
                assert column in event
                # Non-existing columns must be included with value None
                if column not in existing_columns:
                    assert event[column] is None

            # Existing but not selected columns must not be included
            for column in existing_columns - columns:
                assert column not in event
