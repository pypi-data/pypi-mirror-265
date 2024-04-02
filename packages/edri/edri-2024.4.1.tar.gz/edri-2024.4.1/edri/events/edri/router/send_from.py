from typing import Optional

from edri.dataclass.event import event
from edri.events.edri.group import Router


@event
class SendFrom(Router):
    id: Optional[str]
