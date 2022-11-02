"""
Interaction with events table
"""

import datetime
from models import Event
from controller import Session, engine
from sqlalchemy import select
from utils import logger


def update_event(event_id : int, start, finish, user_id : int):
    session = Session()

    event = get_init_event(event_id)
    event = session.execute(event).scalar()

    print('editing')

    if event.user_id != user_id:
        return
    
    print('editing accepted')

    s = datetime.datetime.fromtimestamp(start / 1000)
    f = datetime.datetime.fromtimestamp(finish / 1000)

    logger.info(s, f)

    setattr(event, "start_timestamp", start / 1000)
    setattr(event, "finish_timestamp", finish / 1000)

    session.commit()

    

def get_init_events(
    user_id: int,
    date,
    start_timestamp: float = None,
    finish_timestamp: float = None,
    topic_id: int = None
) -> list:
    events = select(Event).where(Event.user_id == user_id)
    session = Session()

    events = events.where(Event.date == date)

    if start_timestamp is not None:
        events = events.where(Event.start_timestamp > start_timestamp)
    if finish_timestamp is not None:
        events = events.where(Event.finish_timestamp < finish_timestamp)
    if topic_id is not None:
        events = events.where(Event.topic_id == topic_id)

    return list(session.scalars(events))


def get_events(
    user_id: int,
    date: str,
    start_timestamp: float = None,
    finish_timestamp: float = None,
    topic_id: int = None
) -> list:
    events = get_init_events(
        user_id, date, start_timestamp, finish_timestamp, topic_id)

    for i in range(len(events)):
        e = events[i]
        events[i] = {
            'id': e.id,
            'title': e.title,
            'link': e.link,
            'description': e.description,
            'start': e.start_timestamp,
            'finish': e.finish_timestamp,
            'topic_id': e.topic_id
        }

    return events


def get_init_event(id: int) -> Event:
    return select(Event).where(Event.id == id)


def get_event(id: int) -> dict:
    session = Session()
    event = get_init_event(id)

    events_ = list(session.scalars(event))

    if not events_:
        return None

    e = events_[0]

    return {
        'id': e.id,
        'title': e.title,
        'link': e.link,
        'description': e.description,
        'start': e.start_timestamp,
        'finish': e.finish_timestamp,
        'topic_id': e.topic_id
    }


def add_event(
    title: str,
    date: str,
    link: str,
    description: str,
    start: float,
    finish: float,
    topic_id: int,
    user_id: int
) -> Event:

    session = Session()

    event = Event(
        title=title,
        date=date,
        link=link,
        description=description,
        start_timestamp=start,
        finish_timestamp=finish,
        topic_id=topic_id,
        user_id=user_id
    )

    session.add(event)
    session.commit()

    return event


def drop_events_table():
    Event.__table__.drop(engine)


def delete_event(event: Event) -> None:
    _session = Session()
    _session.delete(event)
    _session.commit()
