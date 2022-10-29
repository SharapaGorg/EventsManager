"""
Interaction with events table
"""

from models import Event
from controller import Session, engine
from sqlalchemy import select

def get_init_events(
    start_timestamp: float = None,
    finish_timestamp: float = None
) -> list:
    events = select(Event)
    session = Session()

    if start_timestamp is not None:
        events = events.where(Event.start_timestamp > start_timestamp)
    if finish_timestamp is not None:
        events = events.where(Event.finish_timestamp < finish_timestamp)

    return list(session.scalars(events))

def get_events(
    start_timestamp: float = None,
    finish_timestamp: float = None
) -> list:
    events = get_init_events(start_timestamp, finish_timestamp)

    for i in range(len(events)):
        e = events[i]
        events[i] = {
            'id' : e.id,
            'title' : e.title,
            'link' : e.link,
            'description' : e.description,
            'start' : e.start_timestamp,
            'finish' : e.finish_timestamp
        }

    return events


def add_event(
    title : str,
    link : str,
    description : str,
    start : float,
    finish : float,
    topic_id : int
) -> Event:
    
    session = Session()

    event = Event(
        title = title,
        link = link,
        description = description,
        start_timestamp = start,
        finish_timestamp = finish,
        topic_id = topic_id
    )

    session.add(event)
    session.commit()

    return event

def drop_events_table():
    Event.__table__.drop(engine)

def delete_event(event : Event) -> None:
    _session = Session()
    _session.delete(event)
    _session.commit()