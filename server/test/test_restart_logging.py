# pylint: disable=no-self-use

'''Restart logging session
'''

from json import dumps
from pathlib import Path
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
             '_name': 'test',
         },
         200,
         None),

        ('unknown-fields-are-ignored',
         {
             '_name': 'test',
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
    async def test_restart_logging(self, fx_client, payload, code, message):

        if payload:
            volume_name = payload.get('_name', 'unnamed')
        else:
            volume_name = 'unnamed'

        n_old_volumes = len([
            volume for volume in
            Path(settings.DATA_DIR).glob('{}*.sqlite3'.format(volume_name))])

        if payload:
            data = dumps(payload)
        else:
            data = None

        response = await fx_client.post(RESTART_URL, data=data)
        assert response.status == code

        if message:
            assert await response.text() == message
            return

        db_filename = '{}.sqlite3'.format(volume_name)
        volume_path = Path(settings.DATA_DIR / db_filename)

        assert volume_path.is_file()

        n_new_volumes = len([
            volume for volume in
            Path(settings.DATA_DIR).glob('{}*.sqlite3'.format(volume_name))])

        assert n_new_volumes == n_old_volumes + 1
