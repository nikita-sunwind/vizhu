'''Database maintenance
'''

import os
from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .settings import DATA_DIR


async def create_log(log_name='unnamed'):
    '''Create event log: Create DB engine and database structure
    '''
    timestamp = '{:.6f}'.format(time())

    db_filename = '{}_{}.sqlite3'.format(timestamp, log_name)
    db_path = DATA_DIR / db_filename

    debug_mode = 'DEBUG' in os.environ
    engine = create_engine('sqlite:///{}'.format(db_path), echo=debug_mode)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session, timestamp
