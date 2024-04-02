from abc import abstractmethod
from time import sleep
from logging import Logger
from multiprocessing import Queue
from multiprocessing.connection import wait, Connection, Pipe
from queue import PriorityQueue
from threading import Thread
from typing import Type, Optional, Callable

from edri.abstract import ManagerBase
from edri.dataclass.event import Event
from edri.dataclass.queue_item import QueueItem
from edri.dataclass.worker import Worker
from edri.events.edri.group import Manager
from edri.events.edri.manager import StreamCreate, StreamMessage, StreamClose, WorkerQuit


class ManagerPriorityBase(ManagerBase):
    """
    An extension of ManagerBase that introduces priority handling for events. This class
    manages events using a priority queue, ensuring that higher-priority events are processed
    before lower-priority ones.

    Attributes:
        event_queue (PriorityQueue[QueueItem]): A priority queue for managing events based on their priority.
        event_worker (Thread): A thread dedicated to handling command execution based on event priority.
        waking_up (tuple[Connection, Connection]): A pair of connections used to wake up the manager when a new worker starts.

    Methods:
        __init__: Initializes the ManagerPriorityBase with an optional router queue and logger.
        _prepare: Prepares the manager by initializing the event queue, event worker thread, and waking up pipe.
        additional_pipes: Property to include the waking_up pipe in the set of additional pipes the manager listens to.
        command_handler: Thread target function that processes events from the priority queue.
        get_priority: Abstract method that must be implemented to define the priority of events.
        run_resolver: Main event loop, enhanced to handle events based on priority.
        start_worker: Overrides the start_worker method to wake up the manager when a new worker is started.
    """

    def __init__(self, router_queue: Optional["Queue[Event]"] = None, logger: Optional[Logger] = None) -> None:
        """
        Initializes the ManagerPriorityBase with an optional router queue and logger, setting up the foundation
        for event priority management.

        Parameters:
            router_queue (Optional[Queue[Event]]): The queue for communicating with the router.
            logger (Optional[Logger]): Logger instance for logging messages.
        """
        super().__init__(router_queue, logger)
        self.event_queue: "PriorityQueue[QueueItem]" = None  # type: ignore
        self.event_worker: Thread = None  # type: ignore
        self.waking_up: tuple[Connection, Connection] = None  # type: ignore

    def _prepare(self) -> None:
        """
        Prepares the manager by initializing the event queue, starting the event worker thread,
        and setting up the waking_up pipe used to signal new work.
        """
        super()._prepare()
        self.event_queue = PriorityQueue()
        self.event_worker = Thread(target=self.command_handler)
        self.event_worker.start()
        self.waking_up = Pipe(duplex=False)

    @property
    def additional_pipes(self) -> set[Connection]:
        """
        Includes the waking_up pipe in the set of additional pipes the manager listens to.

        Returns:
            set[Connection]: A set of additional pipes, including the waking_up pipe.
        """
        return {self.waking_up[0]}

    def command_handler(self) -> None:
        """
         The thread target function that processes events from the priority queue, ensuring that events are handled
         in order of their priority.
         """
        while True:
            event = self.event_queue.get().item
            self.resolve(event)

    @abstractmethod
    def get_priority(self, event: Type[Event]) -> int:
        """
        Abstract method that determines the priority of an event. Must be implemented by subclasses
        to define how event priorities are assigned.

        Parameters:
            event (Type[Event]): The class of the event for which the priority needs to be determined.

        Returns:
            int: The priority of the event.
        """
        pass

    def run_resolver(self) -> None:
        """
        The main event loop for the manager, enhanced to handle events based on priority. It listens on all pipes,
        including the waking_up pipe, to efficiently process and prioritize events.
        """
        while True:
            pipes = self.get_pipes()
            if not pipes:
                sleep(1)
                continue
            try:
                active_pipes: list[Connection] = wait(pipes, timeout=10)
                for active_pipe in active_pipes:
                    if active_pipe == self.router_pipe:
                        event: Event = self.router_pipe.recv()
                        self.logger.debug("Přijata zpráva z routeru: %s", event)
                        priority = self.get_priority(event.__class__)
                        self.event_queue.put(QueueItem(priority, event))
                    elif active_pipe == self.waking_up[0]:
                        self.waking_up[0].recv()
                        self.logger.debug("Načtení nových rour")
                        continue
                    else:
                        try:
                            event = active_pipe.recv()
                            self.logger.debug("Přijata zpráva: %s", event)
                        except EOFError as e:
                            self.logger.error("Problém s komunikací", exc_info=e)
                            continue
                        except OSError as e:
                            self.logger.error("Problém v OS", exc_info=e)
                            continue
                        try:
                            key, worker = self._find_worker(active_pipe)
                            if isinstance(event, Manager):
                                if isinstance(event, StreamCreate):
                                    self._resolve_callback_stream_create(event, worker)
                                elif isinstance(event, StreamMessage):
                                    self._resolve_callback_stream_message(event, worker)
                                elif isinstance(event, StreamClose):
                                    self._resolve_callback_stream_close(event, worker)
                                elif isinstance(event, WorkerQuit):
                                    self._remove_worker(key)
                            else:
                                self.resolve_callback_worker(event, worker)
                        except ValueError:
                            self.resolve_callback_pipe(event, active_pipe)
            except KeyboardInterrupt:
                return

    def start_worker(self, event: Event, resolver: Callable, *args, **kwargs) -> Worker:
        """
        Starts a worker to handle an event and signals the manager that new work has started,
        potentially affecting the priority queue.

        Parameters:
            event (Event): The event to be handled by the worker.
            resolver (Callable): The function that will handle the event.
            *args: Additional positional arguments for the resolver.
            **kwargs: Additional keyword arguments for the resolver.

        Returns:
            Worker: The worker instance that was started to handle the event.
        """
        worker = super().start_worker(event, resolver, *args, **kwargs)
        self.waking_up[1].send(None)
        return worker
