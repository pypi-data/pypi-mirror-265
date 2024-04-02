from pickle import loads
from threading import Thread
from queue import Queue
from socket import SHUT_RDWR
from logging import getLogger

from edri.config.constant import SWITCH_NEW_DEMANDS, SWITCH_LAST_MESSAGES
from edri.dataclass.switch import Connection
from edri.events.edri.switch import Demands, LastMessages


class Receiver(Thread):
    def __init__(self, forwarder_queue: "Queue[Event]", connection_id: int, connection: Connection) -> None:
        super(Receiver, self).__init__()
        self.forwarder_queue = forwarder_queue
        self.connection = connection
        self.connection_id = connection_id
        self.logger = getLogger(f"Receiver {connection_id}")

    def run(self) -> None:
        try:
            while True:
                try:
                    recipient_bytes = self.connection.socket.recv(8)
                except ConnectionResetError:
                    self.logger.error("Klient ukončil spojení", )
                    return
                if not recipient_bytes:
                    self.connection.socket.shutdown(SHUT_RDWR)
                    self.logger.error("Ukončeno spojení se switchem", )
                    return
                recipient = int.from_bytes(recipient_bytes, "big", signed=False)
                self.logger.debug("Nová zpráva pro %s", recipient)

                if recipient_bytes == SWITCH_NEW_DEMANDS:
                    self.logger.debug("Nové požadavky")
                    demands_size_bytes = self.connection.socket.recv(8)
                    demands_size = int.from_bytes(demands_size_bytes, "big", signed=False)

                    demands_bytes = self.connection.socket.recv(demands_size)
                    demands = loads(demands_bytes)
                    self.connection.demands = demands
                    self.logger.debug("Požadavky %s", demands)
                    demands_switch = Demands(connection_id=self.connection_id, demands=demands)
                    self.forwarder_queue.put((0, demands_switch))
                elif recipient_bytes == SWITCH_LAST_MESSAGES:
                    self.logger.debug("Poslední zprávy")
                    last_messages_size_bytes = self.connection.socket.recv(8)
                    demands_size = int.from_bytes(last_messages_size_bytes, "big", signed=False)

                    last_messages_bytes = self.connection.socket.recv(demands_size)
                    last_messages = loads(last_messages_bytes)

                    last_messages_switch = LastMessages(connection_id=self.connection_id,
                                                        last_messages=last_messages.get_response().data["last_messages"])
                    self.forwarder_queue.put((0, last_messages_switch))

                else:
                    message_size_bytes = self.connection.socket.recv(8)
                    message_size = int.from_bytes(message_size_bytes, "big", signed=False)

                    message_bytes = self.connection.socket.recv(message_size)

                    self.logger.debug("přijato od %s %sb", recipient, len(message_bytes))
                    self.forwarder_queue.put((recipient, message_bytes))
        except Exception as e:
            self.logger.error("Neznámá chyba", exc_info=e)
