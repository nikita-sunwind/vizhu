'''Signal handlers
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


async def init_db(app):
    '''Configure database engine, create or update database structure
    and initialize ORM session maker
    '''
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    app['engine'] = engine
    app['Session'] = Session


def setup_signal_handlers(app):
    '''Configure signal handlers
    '''
    app.on_startup.append(init_db)
