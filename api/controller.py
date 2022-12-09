from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
import os, logging

engine = create_engine('sqlite:///base')
Base.metadata.create_all(engine)

if not os.path.isfile("./base"):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
