'''Server view handlers
'''

from json import dumps
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
