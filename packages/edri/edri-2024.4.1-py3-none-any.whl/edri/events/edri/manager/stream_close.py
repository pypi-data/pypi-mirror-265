from typing import Type

from edri.dataclass.event import Event, event
from edri.events.edri.group import Manager


@event
class StreamClose(Manager):
    message: Type[Event]
