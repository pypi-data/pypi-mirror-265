from abc import ABC, abstractmethod
from logging import getLogger
from multiprocessing import Pipe, Queue
from multiprocessing.connection import Connection
from typing import Tuple

from edri.events.api.client import Register, Unregister
from edri.config.constant import ApiType


class APIBase(ABC):
    """
    An abstract base class for API components in a system that uses multiprocessing
    for communication between different parts of the application. This class provides
    the basic infrastructure for registering and unregistering clients via a message
    queue.

    Attributes:
        ab_queue (Queue): A multiprocessing queue used for communication between the
        API component and its clients.
        logger (Logger): A logging.Logger instance for logging messages. The logger
        is named after the API.

    Methods:
        __init__(ab_queue: "Queue[Event]"): Constructor for APIBase.
        name: Abstract property. Must be implemented to return the name of the API.
        register(): Attempts to register a client and returns a connection and key.
        type: Abstract property. Must be implemented to return the type of the API.
        unregister(client_pipe: Pipe, key: str): Unregisters a client based on the key.

    Abstract Methods:
        name: Should return the name of the API, mainly used for logging purposes.
        type: Should return the specific ApiType of the API.

    Usage:
        This class must be subclassed and the abstract properties `name` and `type`
        must be implemented. The register and unregister methods provide a mechanism
        for client management, including initiating and closing communication channels.
    """
    def __init__(self, ab_queue: "Queue[Event]") -> None:
        """
        Initializes the APIBase instance with a communication queue.

        Parameters:
            ab_queue (Queue): The multiprocessing queue for inter-process communication.
        """
        super().__init__()
        self.ab_queue = ab_queue
        self.logger = getLogger(self.name)

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Abstract property that should return the name of the API. This name is used
        primarily for logging purposes.

        Returns:
            str: The name of the API.
        """
        pass

    def register(self) -> Tuple[Connection, str] | None:
        """
        Attempts to register a new client with the API. This involves sending a
        registration request through the queue and waiting for a response.

        Returns:
            Tuple[Connection, str] | None: A tuple containing the client connection
            and a registration key if registration is successful; None otherwise.
        """
        client_pipe, client_ab_pipe = Pipe()
        self.ab_queue.put(Register(socket=client_ab_pipe, type=self.type))
        if not client_pipe.poll(timeout=10):
            self.logger.critical("Client registration timeout!")

            client_pipe.close()
            return None
        message = client_pipe.recv()
        if not isinstance(message, Register):
            self.logger.critical("Client registration failed!")
            client_pipe.close()
            return None
        if not message._key:
            self.logger.critical("Key is missing, client registration failed!")
            client_pipe.close()
            return None
        client_ab_pipe.close()
        self.logger.debug("Client was registered %s", message._key)
        return client_pipe, message._key

    @property
    @abstractmethod
    def type(self) -> ApiType:
        """
        Abstract property that should return the type of the API, as defined by the
        ApiType enum. This type is used to identify the API's functionality.

        Returns:
            ApiType: The type of the API.
        """
        pass

    def unregister(self, client_pipe: Connection, key: str) -> None:
        """
        Unregisters a client based on the provided key and closes their communication pipe.

        Parameters:
            client_pipe (Connection): The communication pipe for the client.
            key (str): The registration key of the client to be unregistered.
        """
        unregister = Unregister()
        unregister._key = key
        self.ab_queue.put(unregister)
        client_pipe.close()
        self.logger.debug("Client has left - %s", key)
