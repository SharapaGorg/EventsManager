"""
Interaction with topics table
"""

from models import Topic
from controller import Session, engine
from sqlalchemy import select

def get_init_topics(
    title : str = None
) -> list:
    topics = select(Topic)
    session = Session()

    if title is not None:
        topics = topics.where(Topic.title == title)

    return list(session.scalars(topics))

def get_topics(
    title : str = None,
) -> list:
    topics = get_init_topics(title)

    for i in range(len(topics)):
        e = topics[i]
        topics[i] = {
            'id' : e.id,
            'title' : e.title
        }

    return topics


def add_topic(
    title : str
) -> Topic:
    
    session = Session()

    topic = Topic(
        title = title
    )

    session.add(topic)
    session.commit()

    return topic

def drop_topics_table():
    Topic.__table__.drop(engine)

def delete_topic(topic : Topic) -> None:
    _session = Session()
    _session.delete(topic)
    _session.commit()