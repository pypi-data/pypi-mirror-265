from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional, TypeVar, Mapping, Any

T = TypeVar("T")


class ResponseStatus(IntEnum):
    NONE = -1
    OK = 0
    FAILED = 1


@dataclass
class Response:
    _status: ResponseStatus = field(init=False, default=ResponseStatus.NONE)
    _error: Optional[str] = field(init=False, default=None)
    _changed: bool | None = field(init=False, default=None)

    @property
    def dict(self) -> Mapping[str, str | ResponseStatus]:
        response = {"_response": self._status}
        if self._error:
            response["error"] = self._error

        return response

    def set_status(self, status: ResponseStatus) -> None:
        self._status = status

    def get_status(self) -> ResponseStatus:
        return self._status

    def __setattr__(self, key: str, value: Any) -> None:
        if self._changed is not None and not self._changed:
            super().__setattr__("_changed", True)
            super().__setattr__("_status", ResponseStatus.OK)
        super().__setattr__(key, value)

    def __post_init__(self) -> None:
        self._changed = False

    def has_changed(self) -> bool:
        return self._changed
