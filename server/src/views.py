# pylint: disable=protected-access

'''Server view handlers
'''

from json import dumps
from json.decoder import JSONDecodeError
from time import time
from uuid import uuid4
from aiohttp import web
from .database import create_log
from .exports import export_to_json, export_to_csv
from .models import Event
from .settings import STATIC_DIR


async def index(_):
    '''Serve index route: return static file index.html
    '''
    return web.FileResponse(STATIC_DIR / 'index.html')


async def load_event(request):
    '''Load event data into the database
    '''
    try:
        user_data = await request.json()
    except JSONDecodeError:
        return web.Response(
            status=400, text='request body is not a valid JSON text')

    # Event ID may be set by user or we will set UUIDv4 automatically
    _id = str(user_data.pop('_id', uuid4()))

    try:
        _series = str(user_data.pop('_series'))
    except KeyError:
        return web.Response(status=400, text='_series name is required')

    try:
        _agent = str(user_data.pop('_agent'))
    except KeyError:
        return web.Response(status=400, text='_agent name is required')

    # Timestamp may be set by user or we will set current time automatically
    _timestamp = float(user_data.pop('_timestamp', time()))

    try:
        forbidden_name = next(
            field_name for field_name in user_data.keys()
            if field_name.startswith('_'))
    except StopIteration:
        pass
    else:
        return web.Response(
            status=400,
            text='field names starting with "_" are reserved, '
                 'please check "{}"'.format(forbidden_name))

    # All remaining fields become user-defined data. It will be serialized
    # into JSON string and stored into _data column
    _data = dumps(user_data)

    event = Event(
        _id=_id, _series=_series, _agent=_agent, _timestamp=_timestamp,
        _data=_data)

    session = request.app['Session']()
    session.add(event)
    session.commit()

    return web.Response(status=200, content_type='application/json')


async def query_events(request):
    '''Query events data from the database according to given parameters
    '''
    session = request.app['Session']()
    db_query = session.query(Event)

    # All query options are optional

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

    # If export format isn't requested explicitly assume JSON
    export_format = request.query.get('format', 'json')

    if export_format == 'json':
        response = await export_to_json(request, db_query)
    elif export_format == 'csv':
        response = await export_to_csv(request, db_query)
    else:
        return web.Response(
            status=400,
            text='unknown export format "{}"'.format(export_format))

    return response


async def restart(request):
    '''Restart logging session: Create new database file
    '''
    try:
        user_data = await request.json()
    except JSONDecodeError:
        log_name = 'unnamed'
    else:
        log_name = user_data.get('_name', 'unnamed')

    Session, timestamp = await create_log(log_name)
    request.app['Session'] = Session

    return web.Response(
        status=200,
        text=dumps({'_timestamp': timestamp}),
        content_type='application/json')
