'''Signal handlers
'''

from .database import create_volume


async def init_db(app):
    '''Initialize database
    '''
    app['Session'] = create_volume('default')


def setup_signal_handlers(app):
    '''Configure signal handlers
    '''
    app.on_startup.append(init_db)
