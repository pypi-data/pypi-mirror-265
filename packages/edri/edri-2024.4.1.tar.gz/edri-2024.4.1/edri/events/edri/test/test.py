from typing import Optional

from edri.dataclass.event import event, response, Response
from edri.events.edri.group import Test as GroupTest


@response
class TestResponse(Response):
    random: Optional[int]

@event
class Test(GroupTest):
    pass
