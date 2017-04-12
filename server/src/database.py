'''Database maintenance
'''

import os
from pathlib import Path
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .settings import DATA_DIR


def create_volume(name):
    '''Create new volume with the given name.
    If volume file already exists, rename it as archive with incremented index
    '''
    db_filename = '{}.sqlite3'.format(name)
    volume_path = Path(DATA_DIR / db_filename)
    if volume_path.exists():
        try:
            last_archive = sorted(Path(DATA_DIR).glob(
                '{}.*.sqlite3'.format(name)))[-1]
        except IndexError:
            last_archive = None

        if last_archive:
            last_index = int(re.match(
                r'^\w+\.(\d+)\.sqlite3$', last_archive.name).group(1))
        else:
            last_index = 0

        volume_path.rename(
            DATA_DIR / '{}.{:04d}.sqlite3'.format(name, last_index+1))

    return connect_volume(name)


def connect_volume(name):
    '''Create engine, database structure and return sessionmaker
    '''
    db_filename = '{}.sqlite3'.format(name)
    volume_path = Path(DATA_DIR / db_filename)

    debug_mode = 'DEBUG' in os.environ
    engine = create_engine('sqlite:///{}'.format(volume_path), echo=debug_mode)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session
