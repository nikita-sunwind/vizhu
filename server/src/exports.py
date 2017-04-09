# pylint: disable=protected-access,no-member

'''Export event data to different output formats
'''

from json import dumps, loads
from aiohttp import web
from .models import Event


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
        print('====================EC', existing_columns, user_data)
        return existing_columns


def get_row(event, user_data, columns):
    '''Return flat dictionary with row values
    '''

    row = dict()
    for column in columns:
        if column in EVENT_ATTRS:
            # Columns from reserved fields
            row[column] = getattr(event, column)
        else:
            # Columns from user-defined data fields, None if does not exist
            row[column] = user_data.get(column, None)

    return row


async def export_to_json(request, db_query):
    '''Export event data to JSON as stream HTTP response
    '''

    # Stream response, send data in chuncks - one event per chunk
    response = web.StreamResponse(status=200)
    await response.prepare(request)

    response.write('['.encode('utf-8'))
    for position, event in enumerate(db_query):

        # Delimiter between JSON array items
        if position > 0:
            response.write(','.encode('utf-8'))

        user_data = loads(event._data)
        columns = get_columns(request, user_data)

        # Write row as JSON object
        row = get_row(event, user_data, columns)
        response.write(dumps(row).encode('utf-8'))

        await response.drain()

    response.write(']'.encode('utf-8'))
    await response.drain()

    return response


async def export_to_csv(request, db_query):
    '''Export event data to CSV as stream HTTP response
    '''

    # Stream response, send data in chuncks - one event per chunk
    response = web.StreamResponse(status=200)
    await response.prepare(request)

    for position, event in enumerate(db_query):

        user_data = loads(event._data)

        # For CSV we have to output the same columns set for all rows
        if position == 0:
            columns = get_columns(request, user_data)

            # Write column names
            column_names = ','.join(columns) + ';'
            response.write(column_names.encode('utf-8'))

        # Write row values
        row = get_row(event, user_data, columns)
        strings = (str(value) for value in row.values())
        row_values = ','.join(strings) + ';'
        response.write(row_values.encode('utf-8'))

        await response.drain()

    return response
