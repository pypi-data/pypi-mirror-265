from multiprocessing.connection import Connection
from typing import Optional

from edri.dataclass.event import event
from edri.events.edri.group import Router


@event
class SubscribedAll(Router):
    pipe: Optional[Connection]
