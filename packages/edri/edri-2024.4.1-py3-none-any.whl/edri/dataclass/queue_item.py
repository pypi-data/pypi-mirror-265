from dataclasses import dataclass, field

from edri.dataclass.event import Event


@dataclass(order=True)
class QueueItem:
    priority: int
    item: Event = field(compare=False)
