# pylint: disable=no-self-use

'''Export event data to different formats
'''

from csv import DictReader
from pytest import mark
from test.utils import EVENTS_URL, BAD_DATA


@mark.usefixtures('fx_load_fixtures')
class TestExportData:
    '''Export event data to different formats
    '''

    test_keys = [
        '_id', '_series', '_agent', '_timestamp',
        'roundtrip_delay', 'bad_data']

    async def test_export_data_default_format(self, fx_client):

        params = {
            'series': 'demo',
        }

        response = await fx_client.get(EVENTS_URL, params=params)

        assert response.status == 200
        assert response.headers['Content-Type'] == 'application/json'

    async def test_export_data_to_json(self, fx_client):

        params = {
            'series': 'demo',
            'format': 'json',
        }

        response = await fx_client.get(EVENTS_URL, params=params)

        assert response.status == 200
        assert response.headers['Content-Type'] == 'application/json'

        results = await response.json()
        assert isinstance(results, list)

        for row in results:
            for key in self.test_keys:
                assert key in row

    async def test_export_data_to_csv(self, fx_client):

        params = {
            'series': 'demo',
            'format': 'csv',
        }

        response = await fx_client.get(EVENTS_URL, params=params)

        assert response.status == 200
        assert response.headers['Content-Type'] == 'text/csv'

        results = await response.text()
        assert isinstance(results, str)

        reader = DictReader(results.splitlines())
        for index, row in enumerate(reader):
            for key in self.test_keys:
                assert key in row
            if index > 0:
                assert row['bad_data'] == BAD_DATA
