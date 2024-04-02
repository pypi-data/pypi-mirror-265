from dataclasses import _process_class, dataclass, _FIELD_BASE, field
from enum import Enum
from inspect import isclass
from pathlib import Path
from types import NoneType
from typing import Type, Union
from typeguard import check_type
from sys import version_info

from edri.config.constant import ApiType
from edri.dataclass.event.response import Response
from edri.dataclass.event.event import Event, BaseIdentification
from edri.utility.function import camel2snake


@dataclass
class ApiEventSharing(Enum):
    SPECIFIC = "SPECIFIC"
    ALL = "ALL"


class Method(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class ApiEvent:
    url: str
    resource: str
    sharing: ApiEventSharing
    event: Type[Event]
    exclude: list[ApiType]


Methods = tuple[Method] | Method

events: list[Event] = list()
api_events: list[ApiEvent] = list()
allowed_types = (str, int, float, bool, Methods, Path)


def api(cls=None, /, *, init=True, repr=True, eq=True, order=False,
        unsafe_hash=False, frozen=False, match_args=True,
        kw_only=False, slots=False, url=None, resource=None, sharing=None, exclude=None, weakref_slot=None):
    def wrapper(cls):
        dataclass = _event(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                           frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots,
                           weakref_slot=weakref_slot)
        for name, field in dataclass.__dataclass_fields__.items():
            if name.startswith("_"):
                continue
            if name == "method":
                check_type(field.default, Methods)
            elif name == "response":
                pass
            elif field.type not in allowed_types and isclass(field.type) and not issubclass(field.type, Enum):
                item_type = getattr(field.type, "__origin__", None)
                item_args = getattr(field.type, "__args__", None)
                if item_type == Union:
                    position = 0 if item_args.index(NoneType) == 1 else 1
                    item_type = item_args[position]
                    if item_type in (list, tuple):
                        item_args = item_type.__args__
                if item_type in (list, tuple):
                    if len(item_args) > 1:
                        raise TypeError("Only one child type is allowed got %s" % len(item_args))
                    elif item_args[0] not in allowed_types and not hasattr(item_args[0], "fromisoformat"):
                        raise TypeError("%s cannot be used as a type for API event" % item_args[0])
                elif item_type not in allowed_types and not hasattr(field.type, "fromisoformat"):
                    raise TypeError("%s cannot be used as a type for API event" % field.type)

        if not hasattr(dataclass, "method"):
            if exclude is None or ApiType.REST not in exclude:
                raise ValueError("Method is required for REST")
        else:
            if not isinstance(dataclass.method, tuple):
                dataclass.method = (dataclass.method,)
        api_events.append(ApiEvent(
            url if url else f"/{camel2snake(dataclass.__name__)}",
            resource if resource else camel2snake(dataclass.__name__).replace("_", "-"),
            sharing if sharing else ApiEventSharing.SPECIFIC,
            dataclass,
            exclude if exclude is not None else []))
        return dataclass

    if cls is None:
        return wrapper

    return wrapper(cls)


def _event(cls, init, repr, eq, order, unsafe_hash, frozen, match_args, kw_only, slots, weakref_slot) -> object:
    response = cls.__annotations__.get("response", False)
    if response:
        attribute = getattr(cls, "response", False)
        if attribute:
            attribute.init = False
            attribute.default_factory = response
        else:
            setattr(cls, "response", field(init=False, default_factory=response))
    if version_info < (3, 11, 0):
        dataclass = _process_class(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                                   frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots)
    else:
        dataclass = _process_class(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                                   frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots,
                                   weakref_slot=weakref_slot)

    return dataclass


def event(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
          match_args=True, kw_only=False, slots=False, weakref_slot=False):
    def wrapper(cls):
        return _event(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                      frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots, weakref_slot=weakref_slot)

    if cls is None:
        return wrapper

    return wrapper(cls)


def _response(cls, init, repr, eq, order, unsafe_hash, frozen, match_args, kw_only, slots, weakref_slot):
    annotations = {}
    for name, value in cls.__annotations__.items():
        annotations[name] = value | None
        attribute = getattr(cls, name, False)
        if attribute:
            setattr(cls, name, field(init=False, default=attribute))
        else:
            setattr(cls, name, field(init=False, default=None))

    if version_info < (3, 11, 0):
        dataclass = _process_class(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                                   frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots)
    else:
        dataclass = _process_class(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                                   frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots,
                                   weakref_slot=weakref_slot)

    return dataclass


def response(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
             match_args=True, kw_only=False, slots=False, weakref_slot=None):
    def wrapper(cls):
        return _response(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                         frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots, weakref_slot=weakref_slot)

    if cls is None:
        return wrapper

    return wrapper(cls)


__all__ = ["Event", "event", "Response", "response"]
