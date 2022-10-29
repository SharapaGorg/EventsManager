from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    Text
)

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    link = Column(Text, nullable=True)
    description = Column(Text)
    start_timestamp = Column(Float)
    finish_timestamp = Column(Float)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    event = relationship("Event")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(Text)
    password = Column(Integer)
    event = relationship("Event")