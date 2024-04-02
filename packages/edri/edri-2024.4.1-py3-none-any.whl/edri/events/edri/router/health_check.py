from edri.dataclass.event import event, Response, response
from edri.events.edri.group import Router


@response
class HealthCheckResponse(Response):
    name: str


@event
class HealthCheck(Router):
    response: HealthCheckResponse
