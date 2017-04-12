# pylint: disable=protected-access,no-member

'''Export event data to different output formats
'''

from collections import OrderedDict
from csv import DictWriter
from io import StringIO
from json import dumps, loads
from aiohttp import web
from .models import Event


DATABASE_PAGESIZE = 1000
NETWORK_PAGESIZE = 100
EVENT_ATTRS = Event.__mapper__.attrs.keys()
EVENT_ATTRS.remove('_data')


def get_columns(request, user_data):
    '''Return list of column names for export
    '''

    # Server should return either all selected columns
    # or all existing columns if no one is selected
    selected_columns = set(request.query.getall('columns', []))
    if selected_columns:
        return selected_columns
    else:
        existing_columns = set(EVENT_ATTRS) | set(user_data.keys())
        return existing_columns


def get_row(event, user_data, columns):
    '''Return flat dictionary with row values
    '''

    row = OrderedDict()
    for column in columns:
        if column in EVENT_ATTRS:
            # Columns from reserved fields
            row[column] = getattr(event, column)
        else:
            # Columns from user-defined data fields, None if does not exist
            row[column] = user_data.get(column, None)

    return row


def page_query(db_query):
    '''DB query pagination: Request huge amount of rows in separate chunks
    '''
    offset = 0
    while True:
        results = False
        for item in db_query.limit(DATABASE_PAGESIZE).offset(offset):
            results = True
            yield item
        if not results:
            break
        offset += DATABASE_PAGESIZE


async def export_to_json(request, db_query):
    '''Export event data to JSON as stream HTTP response
    '''

    # Stream response, send data in chuncks
    response = web.StreamResponse(status=200)
    response.content_type = 'application/json'
    await response.prepare(request)

    response.write('['.encode('utf-8'))
    for position, event in enumerate(page_query(db_query)):

        # Delimiter between JSON array items
        if position > 0:
            response.write(','.encode('utf-8'))

        user_data = loads(event._data)
        columns = get_columns(request, user_data)

        # Write row as JSON object
        row = get_row(event, user_data, columns)
        response.write(dumps(row).encode('utf-8'))

        if position % NETWORK_PAGESIZE == NETWORK_PAGESIZE - 1:
            # Drain response chunk
            await response.drain()

    response.write(']'.encode('utf-8'))
    await response.drain()

    return response


async def export_to_csv(request, db_query):
    '''Export event data to CSV as stream HTTP response
    '''

    # Stream response, send data in chuncks
    response = web.StreamResponse(status=200)
    response.content_type = 'text/csv'
    await response.prepare(request)

    buffer = StringIO()
    for position, event in enumerate(page_query(db_query)):

        user_data = loads(event._data)

        # For CSV we have to output the same columns set for all rows
        if position == 0:
            columns = get_columns(request, user_data)
            writer = DictWriter(buffer, fieldnames=columns)

            # Write column names
            writer.writeheader()

        # Write row values
        row = get_row(event, user_data, columns)
        writer.writerow(row)

        if position % NETWORK_PAGESIZE == NETWORK_PAGESIZE - 1:
            # Write data from temporary buffer to response
            response.write(buffer.getvalue().encode('utf-8'))

            # Clear temporary buffer and drain response chunk
            buffer.truncate(0)
            buffer.seek(0)
            await response.drain()

    buffer.close()
    await response.drain()

    return response
