from logging import getLogger
from pickle import dumps
from threading import Thread
from typing import Dict
from queue import Queue


from edri.dataclass.switch import Connection
from edri.events.edri.switch import Demands, LastMessages


class Forwarder(Thread):
    def __init__(self, forwarder_queue: "Queue[Event]", connections: Dict[int, Connection]) -> None:
        super(Forwarder, self).__init__()
        self.forwarder_queue = forwarder_queue
        self.connections = connections
        self.logger = getLogger("Forwarder")

    def run(self) -> None:
        while True:
            receiver, message = self.forwarder_queue.get()
            connection = self.connections.get(receiver)
            if connection:
                self.logger.debug("Předávání zprávy %s", receiver)
                connection.queue.put(message)
            else:
                self.logger.debug("Speciální požadavek")
                if isinstance(message, Demands):
                    self.logger.debug("Nové požadavky od routeru")
                    for connection_id, connection in self.connections.items():
                        if connection_id != message.connection_id:
                            connection.queue.put(dumps(message))
                elif isinstance(message, LastMessages):
                    self.logger.debug("Žádost o odeslání posledních zpráv")
                    for connection_id, connection in self.connections.items():
                        if connection_id != message.connection_id:
                            connection.queue.put(dumps(message))
                else:
                    self.logger.warning("Neznámý požadavek")
