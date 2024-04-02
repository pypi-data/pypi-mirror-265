from edri.dataclass.event import event
from edri.events.edri.group import Switch
from edri.events.edri.router import Demands as RouterDemands


@event
class Demands(Switch):
    connection_id: int
    demands: RouterDemands
