from logging import getLogger
from pickle import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, SOL_SOCKET, SO_KEEPALIVE, IPPROTO_TCP, TCP_KEEPIDLE, \
    TCP_KEEPINTVL, TCP_KEEPCNT
from time import sleep

from edri.dataclass.event import Event
from edri.config.setting import SWITCH_HOST, SWITCH_PORT

SWITCH_BYTES_LENGTH = 8
SWITCH_MAX_SIZE = 2 ** SWITCH_BYTES_LENGTH


class Socket:

    def __init__(self) -> None:
        self.logger = getLogger('Connector.socket')

    def reconnect(self) -> None:
        while True:
            self.logger.debug("Connecting to switch...")
            self.switch_socket = socket(AF_INET, SOCK_STREAM)
            self.switch_socket.settimeout(10)
            self.switch_socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            self.switch_socket.setsockopt(IPPROTO_TCP, TCP_KEEPIDLE, 1)
            self.switch_socket.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, 1)
            self.switch_socket.setsockopt(IPPROTO_TCP, TCP_KEEPCNT, 3)
            try:
                self.switch_socket.connect((SWITCH_HOST, SWITCH_PORT))
                self.switch_socket.settimeout(None)
                self.logger.info("Connected")
                break
            except ConnectionRefusedError as e:
                self.logger.warning("Connection failed - connection was refused", exc_info=e)
                sleep(5)
            except TimeoutError as e:
                self.logger.warning("Connection failed - connection takes too long", exc_info=e)
                sleep(5)
            except Exception as e:
                self.logger.warning("Connection failed - unknown error", exc_info=e)
                sleep(10)

    def send(self, event: Event) -> None:
        data = dumps(event)
        message = len(data).to_bytes(SWITCH_BYTES_LENGTH, "big", signed=False)
        message += data
        if len(message) > SWITCH_MAX_SIZE:
            self.logger.error("Message is too big!")
            return
        self.switch_socket.send(message)

    def _load(self, amount: int) -> bytes:
        data = bytes()
        while len(data) < amount:
            data += self.switch_socket.recv(amount - len(data))

        return data

    def receive(self) -> Event:
        while True:
            message_size_bytes = self._load(8)
            if not message_size_bytes:
                self.switch_socket.shutdown(SHUT_RDWR)
                self.switch_socket.close()
                self.logger.error("Received no message size")
                raise ConnectionError

            message_size = int.from_bytes(message_size_bytes, "big", signed=False)
            self.logger.debug("Receiving size message: %s", message_size)
            message = self._load(message_size)
            try:
                event: Event = loads(message)
            except ModuleNotFoundError as e:
                self.logger.error("Event file was not found", exc_info=e)
            except AttributeError as e:
                self.logger.error("Event is not the same", exc_info=e)
            except Exception as e:
                self.logger.critical("Unknown error while loading Event", exc_info=e)
            else:
                self.logger.debug("Received: %s", event)

                event._switch = True
                return event
