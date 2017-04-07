'''Main server module
'''

import asyncio
import os
from aiohttp import web
from .loggers import setup_loggers
from .routes import setup_routes
from .signal_handlers import setup_signal_handlers


def init_app():
    '''Initialize server application
    '''
    app = web.Application(loop=asyncio.get_event_loop())

    if 'DEBUG' in os.environ:
        setup_loggers()

    setup_routes(app)
    setup_signal_handlers(app)

    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='localhost', port=8080)
