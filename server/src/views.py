# pylint: disable=protected-access,no-member

'''Server view handlers
'''

from json import loads, dumps
from pathlib import Path
from time import time
from uuid import uuid4
from aiohttp import web
from .models import Event


STATIC_PATH = Path.cwd().parent / 'client' / 'dist'


async def index(_):
    '''Serve index route: return static file index.html
    '''
    return web.FileResponse(STATIC_PATH / 'index.html')


async def load_event(request):
    '''Load event data into the database
    '''
    user_data = await request.json()
    print(user_data)

    _id = str(user_data.pop('_id', uuid4()))

    try:
        _series = str(user_data.pop('_series'))
    except KeyError:
        return web.Response(status=400, text='_series name is required')

    try:
        _agent = str(user_data.pop('_agent'))
    except KeyError:
        return web.Response(status=400, text='_agent name is required')

    _timestamp = float(user_data.pop('_timestamp', time()))
    _data = dumps(user_data)

    event = Event(
        _id=_id, _series=_series, _agent=_agent, _timestamp=_timestamp,
        _data=_data)

    session = request.app['Session']()
    session.add(event)
    session.commit()

    return web.Response(status=200)


async def query_events(request):
    '''Query events data from the database according to given parameters
    '''
    session = request.app['Session']()
    db_query = session.query(Event)

    if 'id' in request.query:
        db_query = db_query.filter(Event._id == request.query['id'])

    if 'series' in request.query:
        db_query = db_query.filter(Event._series == request.query['series'])

    if 'agent' in request.query:
        db_query = db_query.filter(Event._agent == request.query['agent'])

    if 'since' in request.query:
        db_query = db_query.filter(Event._timestamp >= request.query['since'])

    if 'till' in request.query:
        db_query = db_query.filter(Event._timestamp <= request.query['till'])

    columns = request.query.getall('columns', None)
    event_attrs = Event.__mapper__.attrs

    output = []
    for event in db_query:

        user_data = loads(event._data)

        if not columns:
            columns = event_attrs.keys() + user_data.keys()

        row = {}
        for column in columns:
            if column in event_attrs.keys():
                row[column] = getattr(event, column)
            else:
                row[column] = user_data.get(column, None)

        output.append(row)

    return web.Response(status=200, text=dumps(output))
