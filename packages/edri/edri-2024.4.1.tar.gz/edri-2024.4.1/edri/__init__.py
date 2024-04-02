from multiprocessing import Queue

from edri.abstract import ManagerBase
from edri.utility.connector import Connector
from edri.utility.scheduler import Scheduler, Job
from edri.config.setting import TOKEN_LENGTH
from edri.dataclass.event import Event
from edri.router import Router
from edri.rest import REST
from edri.utility.store import Store
from edri.utility.api_broker import ApiBroker
from edri.websocket import API as WebSocket


class EDRI:
    def __init__(self) -> None:
        self.router_queue: "Queue[Event]" = Queue()
        self.components: set[ManagerBase] = set()
        self.store: Store
        self.scheduler: Scheduler
        self.rest: REST
        self.websocket: WebSocket
        self.api_broker: ApiBroker
        self.connector: Connector
        self.router: Router

    def add_component(self, component: ManagerBase) -> None:
        self.components.add(component)

    def start_store(self) -> None:
        self.store = Store(self.router_queue)
        self.store.start()

    def start_scheduler(self, jobs: list[Job] | None = None) -> None:
        if not jobs:
            jobs = []
        self.scheduler = Scheduler(self.router_queue, jobs)
        self.scheduler.start()

    def api_broker_start(self) -> None:
        self.api_broker = ApiBroker(self.router_queue, Queue())
        self.api_broker.start()

    def start_rest(self) -> None:
        if not hasattr(self, "api_broker"):
            self.api_broker_start()
        self.rest = REST(self.api_broker.api_broker_queue)
        self.rest.start()

    def start_websocket(self) -> None:
        if not hasattr(self, "api_broker"):
            self.api_broker_start()
        self.websocket = WebSocket(self.api_broker.api_broker_queue)
        self.websocket.start()

    def start_connector(self) -> None:
        self.connector = Connector(self.router_queue)
        self.connector.start()

    def run(self) -> None:
        self.router = Router(self.router_queue, self.components)
        for component in self.components:
            component.start(self.router_queue)
        try:
            self.router.run()
        except KeyboardInterrupt:
            self.router.quit()
