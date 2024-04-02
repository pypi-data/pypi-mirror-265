from dataclasses import dataclass
from queue import Queue
from typing import Optional
from socket import socket

from edri.dataclass.event import Event

from edri.events.edri.router import Demands


@dataclass
class Connection:
    queue: Queue[Event]
    socket: socket
    demands: Optional[Demands]
