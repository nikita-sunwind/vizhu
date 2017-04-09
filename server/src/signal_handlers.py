'''Signal handlers
'''

from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .settings import DATA_DIR


async def init_db(app, session_name='unnamed'):
    '''Configure database engine, create or update database structure
    and initialize ORM session maker
    '''
    timestamp = '{:.6f}'.format(time())
    db_filename = '{}_{}.sqlite3'.format(timestamp, session_name)
    db_path = DATA_DIR / db_filename

    engine = create_engine('sqlite:///{}'.format(db_path), echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    app['engine'] = engine
    app['Session'] = Session

    return timestamp


def setup_signal_handlers(app):
    '''Configure signal handlers
    '''
    app.on_startup.append(init_db)
