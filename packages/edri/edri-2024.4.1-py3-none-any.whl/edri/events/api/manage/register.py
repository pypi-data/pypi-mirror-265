from edri.config.constant import ApiType
from edri.dataclass.event import api, Methods, Method, Response, response
from edri.events.api.group import Manage


@response
class RegisterResponse(Response):
    pass


@api(resource="register", exclude=[ApiType.REST])
class Register(Manage):
    events: list[str]
    parameters: list[str]
    values: list[str]
    # method: Methods = Method.PUT
    response: RegisterResponse
