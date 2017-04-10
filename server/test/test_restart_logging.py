# pylint: disable=no-self-use

'''Restart logging session
'''

from json import dumps
from uuid import uuid4
from pytest import mark
import src.settings as settings
from test.utils import RESTART_URL, unzip_test_cases


class TestRestartLogging:
    '''Restart logging session
    '''

    action_cases = [

        ('can-restart-session-without-name',
         None,
         200,
         None),

        ('can-restart-session-with-name',
         {
             '_name': 'session-{}'.format(uuid4()),
         },
         200,
         None),

        ('unknown-fields-are-ignored',
         {
             '_name': 'session-{}'.format(uuid4()),
             'weird': 'things',
         },
         200,
         None),

        ('empty-json-is-ok',
         {
         },
         200,
         None),

    ]

    ids, argvalues = unzip_test_cases(action_cases)

    @mark.parametrize('payload,code,message', argvalues, ids=ids)
    async def test_can_query_data(self, fx_client, payload, code, message):

        if payload:
            data = dumps(payload)
        else:
            data = None

        response = await fx_client.post(RESTART_URL, data=data)
        assert response.status == code

        if message:
            assert await response.text() == message
            return

        result = await response.json()
        assert isinstance(result, dict)
        assert '_timestamp' in result

        timestamp = result['_timestamp']
        if payload:
            log_name = payload.get('_name', 'unnamed')
        else:
            log_name = 'unnamed'

        db_filename = '{}_{}.sqlite3'.format(timestamp, log_name)
        db_path = settings.DATA_DIR / db_filename

        assert db_path.is_file()
