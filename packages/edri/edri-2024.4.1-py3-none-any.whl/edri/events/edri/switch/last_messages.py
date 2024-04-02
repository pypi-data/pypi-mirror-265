
from typing import Dict

from edri.dataclass.event import event
from edri.events.edri.group import Switch


@event
class LastMessages(Switch):
    connection_id: int
    last_messages: Dict[int, str]
