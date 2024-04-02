from logging import getLogger
from multiprocessing.connection import Connection
from typing import Optional, List, Type, Generic, TypeVar
from abc import abstractmethod

from edri.dataclass.event import Event
from edri.config.constant import STREAM_CLOSE_MARK
from edri.events.edri.manager import StreamCreate, StreamMessage, StreamClose
from edri.events.edri.manager.worker_quit import WorkerQuit

T = TypeVar('T', bound=Event)


class Worker(Generic[T]):
    """
    A generic worker class designed to communicate with a manager through events. It supports sending and receiving messages,
    creating message streams for continuous communication, and handling the lifecycle of these streams.

    Attributes:
        _buffer (List[Event]): A buffer for storing received events that are not yet processed.
        _manager_pipe (Connection): The communication pipe to the manager.
        _name (str): The name of the worker, used for logging purposes.
        _stream_buffer (Optional[Event]): A buffer for the last received stream event.
        _stream_key (Optional[str]): The unique key identifying the current stream.
        event (EventType): The initial event associated with the worker.
        logger (Logger): Logger instance for logging messages.

    Methods:
        __init__: Initializes a new Worker instance.
        do: Abstract method defining the main logic of the worker; to be implemented by subclasses.
        message_send: Sends a message to the manager.
        message_receive: Receives a message from the manager, blocking if no message is available.
        run: Entry point for the worker's execution, wrapping the `do` method with error handling and cleanup.
        stream_close: Closes the current message stream.
        stream_create: Initiates a stream for sending and receiving messages of a specific type.
        stream_exists: Checks if a message stream currently exists.
        stream_poll: Checks if there are messages available in the stream.
        stream_receive: Receives a message from the stream.
        stream_send: Sends a message through the stream.
        stream_wait: Waits for a message in the stream, with an optional timeout.
    """
    def __init__(self, pipe: Connection, event: T, name: str) -> None:
        """
        Initializes a new Worker instance.

        Parameters:
            pipe (Connection): The communication pipe to the manager.
            event (EventType): The initial event associated with this worker.
            name (str): A name for the worker, used for logging.
        """
        self._buffer: List[Event] = []
        self._manager_pipe = pipe
        self._name = name
        self._stream_buffer: Optional[Event] = None
        self._stream_key: Optional[str] = None
        self.event = event
        self.logger = getLogger(self._name)
        if event._stream:
            self._stream_key = event._stream

    @abstractmethod
    def do(self) -> None:
        """
        Abstract method that should be implemented by subclasses to define the worker's main logic.
        """
        pass

    def message_send(self, message: Event) -> None:
        """
        Sends a message to the manager.

        Parameters:
            message (Event): The event to be sent.
        """
        self._manager_pipe.send(message)
        self.logger.debug("Event was sent: %s", message)

    def message_receive(self) -> Event:
        """
        Receives a message from the manager. This method blocks until a message is available.

        Returns:
            Event: The received message.
        """
        if self._buffer:
            return self._buffer.pop(0)
        while True:
            message: Event = self._manager_pipe.recv()
            if isinstance(message, StreamClose):
                if self._stream_key == message._stream:
                    self._stream_key = None
                    self.logger.debug("Stream closed")
                else:
                    self.logger.warning("Wrong key for closing stream: %s", message._stream)
                continue
            else:
                return message

    def run(self) -> None:
        """
        The main entry point for the worker's execution. It calls the `do` method and handles any exceptions,
        ensuring proper cleanup and communication with the manager upon termination.
        """
        try:
            self.do()
        except Exception as e:
            self.logger.error("Worker %s was closed unexpectedly", self._name, exc_info=e)
        finally:
            worker_quit = WorkerQuit()
            self._manager_pipe.send(worker_quit)

    def stream_close(self, message: Optional[Type[Event]] = None) -> bool:
        """
        Closes the current message stream, optionally sending a final message as part of the closure process.

        Parameters:
            message (Optional[Type[Event]]): The type of the final message to send before closing the stream, if any.

        Returns:
            bool: True if the stream was successfully closed; False if there was an issue closing the stream.
        """
        self.logger.debug("Closing the stream...")
        if not self._stream_key:
            self.logger.warning("Key was not provided")
            return False
        self.logger.debug("Stream uzavřen: %s", self._stream_key)
        stream_close = StreamClose(message=message)
        stream_close._stream = self._stream_key
        self.message_send(stream_close)
        return True

    def stream_create(self, message: Event) -> bool:
        """
        Initiates a message stream for continuous communication with the manager, or potentially other workers,
        using a specific type of message.

        Parameters:
            message (Event): The initial message for which the stream is to be created.

        Returns:
            bool: True if the stream was successfully created; False otherwise.
        """
        stream_create = StreamCreate(message=message)
        self.message_send(stream_create)
        stream_create = self.message_receive()
        if stream_create._response._status != 0:
            return False
        self._stream_key = stream_create._stream
        return True

    @property
    def stream_exists(self) -> bool:
        """
        Checks whether a message stream is currently active for this worker.

        Returns:
            bool: True if a stream exists; False otherwise.
        """
        return self._stream_key is not None

    def stream_poll(self) -> bool:
        """
        Non-blocking check to determine if there are messages available in the current stream.

        Returns:
            bool: True if there is at least one message available in the stream; False otherwise.
        """
        if self._stream_buffer:
            return True
        while self._manager_pipe.poll():
            message = self._manager_pipe.recv()
            if message._stream:
                self._stream_buffer = message
                return True
            else:
                self._buffer.append(message)
        return False

    def stream_receive(self) -> Event:
        """
        Receives a message from the current stream. This method should be called after confirming that a message
        is available via `stream_poll` or `stream_wait`.

        Returns:
            Event: The next message from the stream.

        Raises:
            BlockingIOError: If called when no messages are available in the stream.
        """
        if self._stream_buffer:
            message = self._stream_buffer
            self._stream_buffer = None
            return message
        else:
            raise BlockingIOError

    def stream_send(self, message: Event) -> None:
        """
        Sends a message through the current stream to the manager or another worker.

        Parameters:
            message (Event): The message to be sent through the stream.
        """
        stream_message = StreamMessage(message=message)
        self._manager_pipe.send(stream_message)

    def stream_wait(self, timeout: Optional[int] = None) -> bool:
        """
         Waits for a message to be available in the stream, optionally with a timeout. This method is blocking
         and will pause execution until a message is received or the timeout is reached.

         Parameters:
             timeout (Optional[int]): The maximum time to wait for a message, in seconds. If None, waits indefinitely.

         Returns:
             bool: True if a message became available in the stream; False if the timeout was reached without receiving a message.
         """
        if self._stream_buffer:
            return True
        while self.stream_exists:
            if self._manager_pipe.poll(timeout) is not None:
                message = self._manager_pipe.recv()
                if message._stream.endswith(STREAM_CLOSE_MARK):
                    self.logger.debug("Stream closed on both ends: %s", message._stream[:-len(STREAM_CLOSE_MARK)])
                    self._stream_key = None
                    return False
                if message._stream:
                    self._stream_buffer = message
                    return True
                else:
                    self._buffer.append(message)

        return False
