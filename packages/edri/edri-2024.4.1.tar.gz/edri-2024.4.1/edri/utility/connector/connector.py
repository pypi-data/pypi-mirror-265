from logging import getLogger
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from multiprocessing.queues import Queue as MPQueue
from pickle import dumps, loads
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, SOL_SOCKET, SO_KEEPALIVE, IPPROTO_TCP, TCP_KEEPIDLE, \
    TCP_KEEPINTVL, TCP_KEEPCNT
from threading import Thread
from time import sleep
from typing import Optional, Type, Dict, Set
from uuid import uuid4

from edri.dataclass.event import Event
from edri.config.constant import SWITCH_NEW_DEMANDS, SWITCH_LAST_MESSAGES
from edri.config.setting import SWITCH_HOST, SWITCH_PORT
from edri.dataclass.event import BaseIdentification
from edri.events.edri.router import SubscribeConnector, SubscribedAll, SubscribedNew, \
    LastEvents, Demands as RouterDemands, SendFrom
from edri.events.edri.switch import Demands as SwitchDemands, LastMessages as SwitchLastMessages
from edri.utility.connector import Socket


class Connector(Process):
    def __init__(self, router_queue: MPQueue) -> None:
        super(Connector, self).__init__()
        self.router_queue = router_queue
        self.local_request: Set[Type[Event]] = set()
        self.local_response: Set[Type[Event]] = set()
        self.remote_request: Dict[Type[Event], Set[int]] = {}
        self.remote_response: Dict[Type[Event], Set[int]] = {}
        self.logger = getLogger("SwitchConnector")
        self.router_pipe: Optional[Connection] = None

        self.switch_socket: Optional[socket] = None

        self.sender_queue: Optional[Queue] = None
        self.sender_thread: Optional[Thread] = None
        self.receiver_thread: Optional[Thread] = None

        self.switch_id = uuid4()
        self.socket = Socket()

    def sender(self) -> None:
        while True:
            message: Event = self.sender_queue.get()
            if message is False:
                break
            message._switch = BaseIdentification(id=self.switch_id)
            self.logger.debug("Sender - %s", message.__class__)
            if message.get_response() is None:
                router_id_list = self.remote_request.get(message.__class__, None)
            else:
                router_id_list = self.remote_response.get(message.__class__, None)
            for router_id in router_id_list:
                self.logger.debug("Odesílání zprávy switchi %s: %s", router_id, message)
                data = router_id.to_bytes(8, "big", signed=False)
                message_bytes = dumps(message)
                data += len(message_bytes).to_bytes(8, "big", signed=False)
                data += message_bytes
                try:
                    self.switch_socket.send(data)
                except BrokenPipeError:
                    self.logger.warning("Zpráva předána do fronty: %s", message)
                    self.sender_queue.put(message)
                    return
        self.logger.error("Sender se ukončil")

    def receiver(self) -> None:
        def load(amount: int) -> Optional[bytes]:
            data = bytes()
            while True:
                data += self.switch_socket.recv(amount - len(data))
                if not data:
                    return None
                elif len(data) == amount:
                    return data

        while True:
            message_size_bytes = load(8)
            if not message_size_bytes:
                self.switch_socket.shutdown(SHUT_RDWR)
                self.switch_socket.close()
                self.logger.error("Spojení se switchem ukončeno")
                return
            message_size = int.from_bytes(message_size_bytes, "big", signed=False)
            self.logger.debug("Příjem zprávy o velikost: %s", message_size)
            message_bytes = load(message_size)
            message: Event = loads(message_bytes)
            self.logger.debug("Příjem zprávy: %s", message)
            if isinstance(message, SwitchDemands):
                self.logger.debug("Přijaty požadavky od switche: %s", message)
                for demand in message.demands.requests:
                    if demand in self.remote_request:
                        self.remote_request[demand].add(message.connection_id)  # je to set, takže na klid
                    else:
                        self.remote_request[demand] = {message.connection_id}
                        subscribe = SubscribeConnector(event=demand, request=True)
                        self.router_queue.put(subscribe)

                for demand in message.demands.responses:
                    if demand in self.remote_response:
                        self.remote_response[demand].add(message.connection_id)  # je to set, takže na klid
                    else:
                        self.remote_response[demand] = {message.connection_id}
                        subscribe = SubscribeConnector(event=demand, request=False)
                        self.router_queue.put(subscribe)
            elif isinstance(message, SwitchLastMessages):
                last_message = message.last_messages.get(self.switch_id, None)
                self.router_queue.put(SendFrom(id=last_message))
            else:
                message._switch = True
                self.logger.info("-> Router %s", message)
                self.router_queue.put(message)

    def send_demands(self) -> None:
        self.logger.info("Odesílání požadavků do switche")
        data = SWITCH_NEW_DEMANDS
        local_messages_bytes = dumps(RouterDemands(
            requests=self.local_request,
            responses=self.local_response
        ))
        data += len(local_messages_bytes).to_bytes(8, "big", signed=False)
        data += local_messages_bytes
        self.switch_socket.send(data)

    def request_last_messages(self) -> None:
        self.router_queue.put(LastEvents())

    def send_last_messages(self, message: LastEvents) -> None:
        self.logger.info("Odesílání žádosti o poslední zprávy")
        data = SWITCH_LAST_MESSAGES
        last_messages_bytes = dumps(message)
        data += len(last_messages_bytes).to_bytes(8, "big", signed=False)
        data += last_messages_bytes
        self.switch_socket.send(data)

    def receive_setting(self) -> None:
        self.logger.debug("Sending message to receive basic setting")
        self.switch_socket.send()

    def send_basic_info(self) -> None:
        self.logger.debug("Odesílání základních dat switchi")
        data = self.switch_id.to_bytes(8, "big", signed=False)
        self.switch_socket.send(data)
        self.send_demands()
        self.request_last_messages()

    def connect(self) -> None:
        while True:
            self.logger.debug("Připojování ke switchi")
            self.switch_socket = socket(AF_INET, SOCK_STREAM)
            self.switch_socket.settimeout(10)
            self.switch_socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            self.switch_socket.setsockopt(IPPROTO_TCP, TCP_KEEPIDLE, 1)
            self.switch_socket.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, 1)
            self.switch_socket.setsockopt(IPPROTO_TCP, TCP_KEEPCNT, 3)
            try:
                self.switch_socket.connect((SWITCH_HOST, SWITCH_PORT))
                self.switch_socket.settimeout(None)
                self.logger.info("Připojeno ke switchi")
                break
            except ConnectionRefusedError as e:
                self.logger.warning("Nelze se připojit ke switchi - připojení odmítnuto", exc_info=e)
                sleep(5)
            except TimeoutError as e:
                self.logger.warning("Nelze se připojit ke switchi - připojování trvalo příliš dlouho", exc_info=e)
                sleep(5)
            except Exception as e:
                self.logger.warning("Nelze se připojit ke switchi - neznámá chyba", exc_info=e)
                sleep(10)

    def run(self) -> None:
        sleep(10)
        self.logger.debug(f"SwitchConnector se spustil!")
        self.connect()

        self.router_pipe, pipe = Pipe(duplex=False)
        subscribed = SubscribedAll(pipe=pipe)
        self.router_queue.put(subscribed)
        while True:
            message = self.router_pipe.recv()
            if isinstance(message, SubscribedAll):
                self.local_request = message.get_response().data["messages"].requests
                self.local_response = message.get_response().data["messages"].responses
                self.logger.debug("Zprávy routeru %s", message)
                break
            else:
                self.logger.error("Neočekávaná příchozí zpráva %s", message)
        pipe.close()

        self.send_basic_info()

        self.receiver_thread = Thread(target=self.receiver)
        self.receiver_thread.start()

        self.sender_queue = Queue()
        self.sender_thread = Thread(target=self.sender)
        self.sender_thread.start()

        while True:
            if self.router_pipe.poll(timeout=5):
                message = self.router_pipe.recv()
                self.logger.debug("<- Router - %s", message)
                if isinstance(message, SubscribedNew):
                    if message.request:
                        self.local_request.add(message.event)
                    else:
                        self.local_response.add(message.event)
                    self.send_demands()
                elif isinstance(message, LastEvents):
                    self.send_demands()
                    self.send_last_messages(message)
                else:
                    self.sender_queue.put(message)
            if not self.receiver_thread.is_alive():
                self.logger.error("Receiver se ukončil, navazuji nové spojení")
                self.sender_queue.put(False)
                sleep(5)
                self.connect()
                self.send_basic_info()
                self.receiver_thread = Thread(target=self.receiver)
                self.receiver_thread.start()

                self.sender_thread = Thread(target=self.sender)
                self.sender_thread.start()
