
from typing import Type, Set

from edri.dataclass.event import Event, event
from edri.events.edri.group import Router


@event
class Demands(Router):
    requests: Set[Type[Event]]
    responses: Set[Type[Event]]
