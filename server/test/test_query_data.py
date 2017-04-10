# pylint: disable=no-self-use

'''Query event data from the server
'''

from json import dumps
from time import time
from uuid import uuid4
from pytest import mark
from test.utils import EVENTS_URL, params_to_multidict, unzip_test_cases


class TestQueryData:
    '''Query event data from the server
    '''

    action_cases = [

        ('can-query-data-with-all-possible-filters',
         {
             'format': 'json',
             'id': str(uuid4()),
             'series': 'series-{}'.format(uuid4()),
             'agent': 'agent-{}'.format(uuid4()),
             'since': str(time() - 1000),
             'till': str(time() + 1000),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-without-filters',
         {
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
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
             'series': 'series-{}'.format(uuid4()),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-agent',
         {
             'agent': 'agent-{}'.format(uuid4()),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-time-period',
         {
             'since': str(time() - 1000),
             'till': str(time() + 1000),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-time-since',
         {
             'since': str(time() - 1000),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-data-by-time-till',
         {
             'till': str(time() + 1000),
             'columns': ['_id', '_timestamp', 'roundtrip_delay'],
         },
         200,
         None),

        ('can-query-nonexistent-column',
         {
             'columns': ['_id', 'weird_column'],
         },
         200,
         None,),

    ]

    ids, argvalues = unzip_test_cases(action_cases)

    @mark.parametrize('params,code,message', argvalues, ids=ids)
    async def test_can_query_data(self, fx_client, params, code, message):

        event_id = params.get('id', str(uuid4()))

        payload = {
            '_id': event_id,
            '_series': params.get('series', 'demo'),
            '_agent': params.get('agent', 'Smith'),
            '_timestamp': time(),
            'roundtrip_delay': 0.001,
        }

        response = await fx_client.post(
            EVENTS_URL, data=dumps(payload))

        assert response.status == 200

        response = await fx_client.get(
            EVENTS_URL, params=params_to_multidict(params))

        assert response.status == code

        if message:
            assert await response.text() == message
            return

        results = await response.json()
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

            # _data column must not be included
            assert '_data' not in event
