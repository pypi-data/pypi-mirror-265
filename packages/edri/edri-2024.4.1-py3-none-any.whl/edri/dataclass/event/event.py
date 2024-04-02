from dataclasses import dataclass, field
from random import choices
from string import ascii_letters, digits
from typing import Optional, TypeGuard, TYPE_CHECKING
from zlib import adler32

from edri.config.setting import SWITCH_KEY_LENGTH
from edri.dataclass.event import Response
from edri.dataclass.event.response import ResponseStatus

if TYPE_CHECKING:
    from typing import TypeVar

    _T = TypeVar("_T")

    class _ResponseExists:
        response: Response


@dataclass
class BaseIdentification:
    id: Optional[int] = None
    key: str = field(default_factory=lambda: "".join(choices(ascii_letters + digits, k=SWITCH_KEY_LENGTH)))
    received: bool = False

    def __repr__(self) -> str:
        return f"{self.id}:{self.key}"


@dataclass
class Event:
    _key: Optional[str] = field(init=False, default=None)
    _stream: Optional[str] = field(init=False, default=None)
    _switch: Optional[BaseIdentification] = field(init=False, default=None)
    _headers: list[tuple[bytes, bytes]] | None = field(init=False, default=None)
    _cookies: dict[str, str] | None = field(init=False, default=None)
    _worker: str | None = field(init=False, default=None)
    response: Optional[Response] = field(init=False, default=None)

    def get_response(self) -> Optional[Response]:
        if self.response and self.response.get_status() != ResponseStatus.NONE:
            return self.response
        return None

    def has_response(self) -> bool:
        return self.response is not None and self.response.get_status() != ResponseStatus.NONE

    def set_response(self, response: Response) -> None:
        self._switch = None
        self.response = response

    def remove_response(self) -> None:
        self._switch = None
        self.response = None

    @classmethod
    def hash_name(cls) -> int:
        base = cls.__class__
        return adler32(f"{base.__module__}.{base.__qualname__}".encode())
