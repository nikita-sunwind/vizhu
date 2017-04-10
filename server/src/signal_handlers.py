'''Signal handlers
'''

from .database import create_log


async def init_db(app):
    '''Initialize database
    '''
    Session, _ = await create_log('unnamed')
    app['Session'] = Session


def setup_signal_handlers(app):
    '''Configure signal handlers
    '''
    app.on_startup.append(init_db)
