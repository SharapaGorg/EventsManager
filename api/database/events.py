"""
Interaction with events table
"""

from models import Event
from controller import Session, engine
from sqlalchemy import select

def get_init_events(
    user_id : int,
    start_timestamp: float = None,
    finish_timestamp: float = None
) -> list:
    events = select(Event).where(Event.user_id == user_id)
    session = Session()

    if start_timestamp is not None:
        events = events.where(Event.start_timestamp > start_timestamp)
    if finish_timestamp is not None:
        events = events.where(Event.finish_timestamp < finish_timestamp)

    return list(session.scalars(events))


def get_events(
    user_id : int,
    start_timestamp: float = None,
    finish_timestamp: float = None
) -> list:
    events = get_init_events(user_id, start_timestamp, finish_timestamp)

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
    link: str,
    description: str,
    start: float,
    finish: float,
    topic_id: int,
    user_id : int
) -> Event:

    session = Session()

    event = Event(
        title=title,
        link=link,
        description=description,
        start_timestamp=start,
        finish_timestamp=finish,
        topic_id=topic_id,
        user_id = user_id
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
