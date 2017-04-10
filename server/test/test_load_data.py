# pylint: disable=no-self-use

'''Load event data to the server
'''

from json import dumps
from time import time
from uuid import uuid4
from pytest import mark
from test.utils import EVENTS_URL, unzip_test_cases


class TestLoadData:
    '''Load event data to the server
    '''

    action_cases = [

        ('can-load-event-with-all-reserved-fields',
         {
             '_id': str(uuid4()),
             '_series': 'demo',
             '_agent': 'Smith',
             '_timestamp': time(),
             'roundtrip_delay': 0.001,
         },
         200,
         None),

        ('can-load-event-with-minimal-fields',
         {
             '_series': 'demo',
             '_agent': 'Smith',
             'roundtrip_delay': 0.001,
         },
         200,
         None),

        ('can-load-event-without-user-data',
         {
             '_series': 'demo',
             '_agent': 'Smith',
         },
         200,
         None),

        ('series-field-is-required',
         {
             '_agent': 'Smith',
         },
         400,
         '_series name is required'),

        ('agent-field-is-required',
         {
             '_series': 'Smith',
         },
         400,
         '_agent name is required'),

        ('cannot-use-reserved-names',
         {
             '_series': 'demo',
             '_agent': 'Smith',
             '_roundtrip_delay': 0.001,
         },
         400,
         'field names starting with "_" are reserved, '
         'please check "_roundtrip_delay"'),

        ('body-must-be-valid-json-text',
         None,
         400,
         'request body is not a valid JSON text'),

    ]

    ids, argvalues = unzip_test_cases(action_cases)

    @mark.parametrize('payload,code,message', argvalues, ids=ids)
    async def test_load_event(self, fx_client, payload, code, message):

        if payload:
            data = dumps(payload)
        else:
            data = None

        response = await fx_client.post(EVENTS_URL, data=data)

        assert response.status == code

        if message:
            assert await response.text() == message
