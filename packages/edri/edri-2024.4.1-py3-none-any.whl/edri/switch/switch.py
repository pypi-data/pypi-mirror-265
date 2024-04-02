from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from logging import getLogger
from typing import Dict
from queue import Queue
from pickle import dumps

from edri.dataclass.switch import Connection
from edri.events.edri.switch import Demands
from edri.switch import Forwarder, Receiver, Sender
from edri.config.setting import SWITCH_HOST, SWITCH_PORT


class Switch:
    def __init__(self) -> None:
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.logger = getLogger(__name__)
        self.connections: Dict[int, Connection] = {}
        self.forwarder_queue = Queue()
        self.forwarder: Forwarder = Forwarder(self.forwarder_queue, self.connections)
        self.forwarder.start()

    def handle_new_connection(self, connection: socket) -> None:
        connection_id_bytes = connection.recv(8)
        connection_id = int.from_bytes(connection_id_bytes, "big", signed=False)
        connection_info = self.connections.get(connection_id)
        self.logger.info("Nové spojení - %s", connection_id)
        if connection_info:
            self.logger.info("Obnova spojení s %s", connection_id)
            connection_info.socket = connection
            receiver = Receiver(self.forwarder_queue, connection_id, connection_info)
            receiver.start()
            sender = Sender(connection_info.queue, connection, connection_id)
            sender.start()
            self.logger.debug("Spuštěn receiver a sender")
        else:
            self.logger.info("Nové spojení s %s", connection.getsockname())
            connection_info = Connection(Queue(), connection, None)
            self.connections[connection_id] = connection_info
            receiver = Receiver(self.forwarder_queue, connection_id, connection_info)
            receiver.start()
            sender = Sender(connection_info.queue, connection, connection_id)
            sender.start()
            self.logger.debug("Spuštěn receiver a sender")

        for connection_id_demand, connection_demand in self.connections.items():
            if connection_id != connection_id_demand:
                demand = dumps(Demands(connection_id=connection_id_demand, demands=connection_demand.demands))
                self.forwarder_queue.put((connection_id, demand))

    def run(self) -> None:
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((SWITCH_HOST, SWITCH_PORT))
        self.socket.listen()
        while True:
            connection, address = self.socket.accept()
            self.logger.debug("Nové spojení s %s", address)
            self.handle_new_connection(connection)


if __name__ == "__main__":
    switch = Switch()
    switch.run()
