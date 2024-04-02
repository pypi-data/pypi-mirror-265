from typing import Optional, Any

from edri.dataclass.event import Event, event, response, Response
from edri.events.edri.group import Store


@response
class GetResponse(Response):
    value: Any


@event
class Get(Store):
    name: str
    data: Optional[Event] = None
    response: GetResponse
