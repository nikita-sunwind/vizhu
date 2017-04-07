'''Data model definition
'''

from sqlalchemy import Column, Float, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Event(Base):
    '''Database model definition: Event
    '''
    __tablename__ = 'events'

    _id = Column(String, primary_key=True)
    _series = Column(String, nullable=False)
    _agent = Column(String, nullable=False)
    _timestamp = Column(Float)
    _data = Column(String)

    def __repr__(self):
        '''Model instance representation
        '''
        return '<Event(_id={}, _series={}, _agent={}, _timestamp={})>'.format(
            self._id, self._series, self._agent, self._timestamp)
