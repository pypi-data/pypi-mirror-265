from datetime import datetime, timedelta
from typing import Union, Optional

from edri.dataclass.event import event, response, Response, Event


@response
class SetResponse(Response):
    identifier: str


@event
class Set(Event):
    event: Event
    when: datetime
    repeat: Optional[timedelta] = None
    identifier: Optional[str] = None
    response: SetResponse
