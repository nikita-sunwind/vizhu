# pylint: disable=no-self-use,no-member

'''Export event data to different formats
'''

from csv import DictReader
from io import BytesIO
import numpy as np
from pytest import mark
from test.utils import EVENTS_URL, BAD_DATA, COMPOUND_DATA, N_TEST_EVENTS


@mark.usefixtures('fx_load_fixtures')
class TestExportData:
    '''Export event data to different formats
    '''

    test_keys = [
        '_id', '_series', '_agent', '_timestamp',
        'roundtrip_delay', 'bad_data', 'compound_data']

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
        assert len(results) == N_TEST_EVENTS

        for row in results:
            for key in self.test_keys:
                assert key in row
            assert row['bad_data'] == BAD_DATA
            assert row['compound_data'] == COMPOUND_DATA

    async def test_export_data_to_csv(self, fx_client):

        params = {
            'series': 'demo',
            'format': 'csv',
        }

        response = await fx_client.get(EVENTS_URL, params=params)

        assert response.status == 200
        assert response.headers['Content-Type'] == 'text/csv'

        results = list()
        async for line in response.content:
            results.append(line.decode('utf-8'))

        assert len(results) == N_TEST_EVENTS + 1

        reader = DictReader(results)
        for index, row in enumerate(reader):
            for key in self.test_keys:
                assert key in row
            if index > 0:
                assert row['bad_data'] == BAD_DATA
                assert row['compound_data'] == str(COMPOUND_DATA)

    async def test_export_data_to_numpy(self, fx_client):

        params = {
            'series': 'demo',
            'format': 'numpy',
        }

        response = await fx_client.get(EVENTS_URL, params=params)

        assert response.status == 200
        assert response.headers['Content-Type'] == 'application/octet-stream'

        received_data = await response.read()

        buffer = BytesIO()
        buffer.write(received_data)

        buffer.seek(0)
        result = np.load(buffer)

        assert result.shape == (N_TEST_EVENTS, len(self.test_keys))

        for row in result:
            assert BAD_DATA in row
            for cell in row:
                if cell == COMPOUND_DATA:
                    break
            else:
                assert False
