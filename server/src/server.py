'''Main server module
'''

import asyncio
import os
from aiohttp import web
from .loggers import setup_loggers
from .routes import setup_routes
from .settings import SERVER_PORT
from .signal_handlers import setup_signal_handlers


def create_app(loop=asyncio.get_event_loop()):
    '''Initialize web application
    '''
    if 'DEBUG' in os.environ:
        setup_loggers()

    app = web.Application(loop=loop)

    setup_routes(app)
    setup_signal_handlers(app)

    return app


if __name__ == '__main__':
    web.run_app(create_app(), host='localhost', port=SERVER_PORT)
