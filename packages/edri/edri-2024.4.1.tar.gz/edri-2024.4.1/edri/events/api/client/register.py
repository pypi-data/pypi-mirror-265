from multiprocessing.connection import Connection

from edri.dataclass.event import event, Response, response
from edri.config.constant import ApiType
from edri.events.api.group import Client


@response
class RegisterResponse(Response):
    pass


@event
class Register(Client):
    socket: Connection
    type: ApiType
    response: RegisterResponse
