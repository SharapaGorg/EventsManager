import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Float,
    Integer,
    Text
)

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    link = Column(Text)
    description = Column(Text)
    start_timestamp = Column(Float)
    finish_timestamp = Column(Float)