from logging import getLogger
from multiprocessing import Queue
from typing import Dict, Any

from edri.dataclass.event import Event
from edri.abstract import ManagerBase
from edri.events.edri.store import Set, Get


class Store(ManagerBase):
    def __init__(self, router_queue: Queue[Event]) -> None:
        super().__init__(router_queue, getLogger(__name__))
        self.store: Dict[str, Any] = {}

    def solve_req_set(self, event: Set) -> None:
        self.store[event.name] = event.value

    def solve_req_get(self, event: Get) -> None:
        event.response.value = self.store.get(event.name, None)
