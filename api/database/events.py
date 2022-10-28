"""
Interaction with events table
"""

from models import Event
from controller import Session
from sqlalchemy import select


def get_events(
    start_timestamp: float = None,
    finish_timestamp: float = None
) -> list:
    events = select(Event)
    session = Session()

    if start_timestamp is not None:
        events = events.where(Event.start_timestamp > start_timestamp)
    if finish_timestamp is not None:
        events = events.where(Event.finish_timestamp < finish_timestamp)

    events = list(session.scalars(events))

    for i in range(len(events)):
        e = events[i]
        events[i] = {
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
    finish : float
) -> Event:
    
    session = Session()

    event = Event(
        title = title,
        link = link,
        description = description,
        start_timestamp = start,
        finish_timestamp = finish
    )

    session.add(event)
    session.commit()

    return event
