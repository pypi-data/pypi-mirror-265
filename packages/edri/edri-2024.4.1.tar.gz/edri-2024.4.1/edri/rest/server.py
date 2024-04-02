import asyncio
from dataclasses import asdict
from enum import Enum
from json import JSONEncoder, dumps, loads
from logging import getLogger
from multiprocessing import Process
from multiprocessing.queues import Queue
from os import remove
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import NoneType
from typing import Type, Any, Union, Pattern
from urllib.parse import parse_qs, quote
from re import compile
from http.cookies import SimpleCookie

from uvicorn import Config, Server

from edri.config.setting import UPLOAD_FILES_PREFIX, REST_RESPONSE_TIMEOUT, REST_PORT
from edri.abstract.api_base import APIBase
from edri.config.constant import ApiType
from edri.dataclass.event import Method, Event, api_events
from edri.dataclass.event.response import ResponseStatus
from edri.utility.function import snake2camel, camel2snake


class REST(Process):
    """
    A process dedicated to running a RESTful API server using Uvicorn, an ASGI server.
    Inherits from multiprocessing.Process to run the API server in a separate process.

    Attributes:
        api_broker_queue (Queue): A multiprocessing queue used for communication with
        the API broker, facilitating the handling of API requests.
        type (ApiType): The type of the API, set to ApiType.REST for RESTful APIs.
        logger (Logger): Logger instance for logging information related to API server
        operations.

    Methods:
        run(): Starts the Uvicorn server with the provided configuration and runs
        the ASGI application to handle RESTful API requests.
    """

    def __init__(self, api_broker_queue: Queue[Event]) -> None:
        """
        Initializes the REST API server process.

        Parameters:
            api_broker_queue (Queue): The queue for communication with the API broker.
        """
        super().__init__()
        self.api_broker_queue = api_broker_queue

        self.type = ApiType.REST
        self.logger = getLogger(__name__)

    class App(APIBase):
        """
        An ASGI application for handling RESTful API requests, translating them
        into events for processing by the system.

        Inherits from APIBase to utilize common API functionalities and to handle
        requests in a structured manner.

        Attributes:
            events (dict): A dictionary mapping API paths to events and their handling
            methods.
            http_codes_mapping (dict): Maps response statuses to HTTP status codes.
        """

        def __init__(self, ab_queue: Queue[Event]) -> None:
            """
            Initializes the ASGI application with a queue for communication and
            predefines the mapping of API events.

            Parameters:
                ab_queue (Queue): The queue for communication with the API broker.
            """
            super().__init__(ab_queue)
            self.events = self.sort_events()
            self.http_codes_mapping = {
                ResponseStatus.OK: 200,
                ResponseStatus.FAILED: 409,
            }

        @staticmethod
        def sort_events() -> dict[str, dict[Method | str, Type[Event] | Pattern[str]]]:
            """
            Organizes API events by their URL and HTTP method for efficient lookup.

            Returns:
                A dictionary organizing events by URL and method.
            """
            data: dict[str, dict] = {}
            url_replace = compile(r"{([^}]+)}")
            for api_event in api_events:
                position = api_event.url.find("{")
                if position == -1:
                    url = api_event.url
                else:
                    url = api_event.url[:position]
                if url not in data:
                    data[url] = dict()
                events = data[url]
                if ApiType.REST in api_event.exclude:
                    continue
                for method in api_event.event.method:
                    if method in events:
                        raise ValueError("Method %s was already set.", method)
                    events[method] = api_event.event
                    if position != -1:
                        events["url"] = compile(url_replace.sub(r"(?P<\1>.+)", api_event.url))
            return data

        @staticmethod
        def get_default_headers(headers: list[tuple[bytes, bytes]], content_type: bytes = b"application/json") -> list[tuple[bytes, bytes]]:
            response_headers: list[tuple[bytes, bytes]] = [
                (b"Access-Control-Allow-Headers", b"Accept,Accept-Language,Content-Language,Content-Type,Filename"),
                (b"Content-Type", content_type)
            ]
            for name, value in headers:
                if name == b"origin":
                    response_headers.append((b"Access-Control-Allow-Origin", value))
                    break

            return response_headers

        @property
        def name(self) -> str:
            """
            Returns the name of the REST API component, used primarily for logging purposes.

            Returns:
                The name of the API component.
            """
            return "edri.api.rest"

        @property
        def type(self) -> ApiType:
            """
            Identifies the API type as REST, aligning with the application's architecture.

            Returns:
                The enumerated type indicating this component handles RESTful API requests.
            """
            return ApiType.REST

        @staticmethod
        def dict_factory(data: list[tuple[str, Any]]) -> dict:
            """
            Converts a list of tuples into a dictionary, handling specific types like Enums
            by converting them to their value.

            Parameters:
                data (list[tuple[str, Any]]): A list of key-value pairs.

            Returns:
                A dictionary with keys mapped to converted values if necessary.
            """

            def convert_value(obj: Any) -> Any:
                if isinstance(obj, Enum):
                    return obj.value
                return obj

            return {key: convert_value(value) for key, value in data}

        class CustomJSONEncoder(JSONEncoder):
            """
            A custom JSON encoder for converting various data types to JSON-compatible
            formats, including support for Enums, datetime objects, Paths, bytes, and
            more.

            Inherits from JSONEncoder to override the default() method for custom serialization.
            """

            def default(self, data) -> Any:
                if hasattr(data, "to_json"):
                    return data.to_json()
                elif hasattr(data, "isoformat"):
                    return data.isoformat()
                elif isinstance(data, Path):
                    return data.as_posix()
                elif isinstance(data, bytes) or isinstance(data, bytearray):
                    return data.hex()
                elif isinstance(data, Enum):
                    return data.value
                else:
                    return super().default(data)

        def check_type(self, values: Any, annotation: Any) -> Any:
            """
            Validates and converts input values to the specified annotation type,
            supporting basic types, Optional, and lists with type annotations.

            Parameters:
                values: The input value to be validated and converted.
                annotation: The target type annotation for the conversion.

            Returns:
                The converted value if conversion is successful.

            Raises:
                TypeError: If the value cannot be converted to the specified type.
            """
            if hasattr(annotation, "__origin__"):
                if annotation.__origin__ == Union:
                    try:
                        none_position = annotation.__args__.index(NoneType)
                    except ValueError:
                        raise TypeError("Unions can consist only of basic type and None")
                    if values is None:
                        return values
                    else:
                        return self.check_type(values, annotation.__args__[0 if none_position == 1 else 1])
                elif annotation.__origin__ == list and isinstance(values, list):
                    if len(annotation.__args__) != 1:
                        raise TypeError("Type of list item must be specified")
                    return [self.check_type(value, annotation.__args__[0]) for value in values]
                else:
                    raise TypeError("Value '%s' cannot be converted to type %s" % (values, annotation))
            else:
                try:
                    return annotation(values)
                except Exception as e:
                    if hasattr(annotation, "fromisoformat"):
                        try:
                            return annotation.fromisoformat(values)
                        except Exception as e:
                            self.logger.debug("Convert error", exc_info=e)
                            raise TypeError("Value '%s' cannot be converted from isoformat to type %s" % (values, annotation))
                    else:
                        self.logger.debug("Convert error", exc_info=e)
                        raise TypeError("Value '%s' cannot be converted to type %s" % (values, annotation))

        async def __call__(self, scope, receive, send) -> None:
            """
            The main entry point for handling incoming HTTP requests as per the ASGI
            specification. Routes requests to the appropriate event based on the URL
            and method, performs data validation, and sends HTTP responses.

            Parameters:
                scope: The scope of the incoming request containing type, path, headers, etc.
                receive: An awaitable callable yielding incoming messages.
                send: An awaitable callable taking outgoing messages.

            Returns:
                None: This method handles the request and sends an HTTP response
                without returning a value.
            """
            if scope["type"] == "lifespan":  # waiting for startup
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})

            elif scope["type"] == "http":
                loop = asyncio.get_event_loop()
                event_constructors = self.events.get(scope["path"], None)
                parameters: dict[str, str] = {}
                if not event_constructors:
                    for url, events in self.events.items():
                        url_re = events.get("url", None)
                        if not url_re:
                            continue
                        if scope["path"].startswith(url):
                            match = url_re.match(scope["path"])
                            parameters.update(match.groupdict())
                            event_constructors = events
                            break
                    else:
                        self.logger.debug("Unknown url %s", scope["path"])
                        await send({
                            'type': 'http.response.start',
                            'status': 400,
                            'headers': [
                                [b'content-type', b'text/plain'],
                            ]
                        })
                        await send({
                            'type': 'http.response.body',
                            'body': b"",
                            'more_body': False
                        })
                        return

                if scope["method"] == "OPTIONS":
                    # to vecpané URL :|
                    headers = self.get_default_headers(scope["headers"])
                    headers.append(
                        (b"Access-Control-Allow-Methods",
                         ", ".join(x.value for x in event_constructors.keys() if x != "url").encode())
                    )
                    await send({
                        'type': 'http.response.start',
                        'status': 200,
                        'headers': headers
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': b"",
                        'more_body': False
                    })
                    return

                method = Method(scope["method"])
                event_constructor = event_constructors.get(method, None)

                if not event_constructor:
                    await send({
                        'type': 'http.response.start',
                        'status': 405,
                        'headers': [
                            [b'content-type', b'text/plain'],
                        ]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': b"",
                        'more_body': False
                    })
                    return

                cookies = None
                for key, value in scope["headers"]:
                    if key == b"cookie":
                        simple_cookies = SimpleCookie()
                        simple_cookies.load(value.decode())
                        cookies = {key: value.value for key, value in simple_cookies.items()}
                        break
                url_parameters = parse_qs(scope["query_string"].decode("utf-8"), keep_blank_values=True)
                parameters.update(
                    {camel2snake(key.strip("[]")): value if key.endswith("[]") else value[-1] for key, value in
                     url_parameters.items()})

                json_request = False
                for key, value in scope["headers"]:
                    if key == b"content-type" and value == b"application/json":
                        json_request = True

                if json_request:
                    raw_data = b""
                    while True:
                        if len(raw_data) > 4096 * 1024:
                            await send({
                                'type': 'http.response.start',
                                'status': 413,
                                'headers': [
                                    [b'content-type', b'text/plain'],
                                ]
                            })
                            await send({
                                'type': 'http.response.body',
                                'body': b"",
                                'more_body': False
                            })
                            return

                        body = await receive()
                        data = body.get("body", None)
                        if data is not None:
                            raw_data += data
                            if not body["more_body"]:
                                break
                        else:
                            break

                    if not raw_data:  # no data = error in json parser - prepare dummy data for it
                        raw_data = b"{}"

                    try:
                        parameters.update({camel2snake(key): value for key, value in loads(raw_data).items()})
                    except Exception as e:
                        self.logger.warning("Cannot process json data", exc_info=e)
                        await send({
                            'type': 'http.response.start',
                            'status': 422,
                            'headers': [
                                [b'content-type', b'text/plain'],
                            ]
                        })
                        await send({
                            'type': 'http.response.body',
                            'body': b"",
                            'more_body': False
                        })
                        return

                    for name, value in parameters.items():
                        annotation = event_constructor.__annotations__.get(name, None)
                        if not annotation:
                            self.logger.debug("Unknown parameter %s", name)
                            await send({
                                'type': 'http.response.start',
                                'status': 400,
                                'headers': [
                                    [b'content-type', b'text/plain'],
                                ]
                            })
                            await send({
                                'type': 'http.response.body',
                                'body': b"",
                                'more_body': False
                            })
                            return
                        try:
                            value = self.check_type(value, annotation)
                        except TypeError as e:
                            self.logger.debug("Wrong type %s for %s:%s", type(value), name, annotation, exc_info=e)
                            await send({
                                'type': 'http.response.start',
                                'status': 400,
                                'headers': [
                                    [b'content-type', b'text/plain'],
                                ]
                            })
                            await send({
                                'type': 'http.response.body',
                                'body': b"",
                                'more_body': False
                            })
                            return
                        except Exception as e:
                            self.logger.debug("Unknown error during type checking", exc_info=e)
                            await send({
                                'type': 'http.response.start',
                                'status': 500,
                                'headers': [
                                    [b'content-type', b'text/plain'],
                                ]
                            })
                            await send({
                                'type': 'http.response.body',
                                'body': b"",
                                'more_body': False
                            })
                            return
                        parameters[name] = value
                else:
                    for key, value in scope["headers"]:
                        if key == b"content-length":
                            try:
                                size = int(value)
                            except Exception:
                                continue
                            if size > 0:
                                temporary_file = NamedTemporaryFile(prefix=UPLOAD_FILES_PREFIX, delete=False)
                                parameters["path"] = Path(temporary_file.name)
                                break

                try:
                    event = event_constructor(**parameters)
                except Exception as e:
                    self.logger.warning("Cannot create event", exc_info=e)
                    if not json_request and "path" in parameters:
                        temporary_file.close()
                        remove(temporary_file.name)
                    await send({
                        'type': 'http.response.start',
                        'status': 400,
                        'headers': [
                            [b'content-type', b'text/plain'],
                        ]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': b"",
                        'more_body': False
                    })
                    return

                if not json_request and "path" in parameters:
                    while True:
                        body = await receive()
                        data = body.get("body", None)
                        if data is not None:
                            temporary_file.write(data)
                            if not body["more_body"]:
                                break
                        else:
                            break
                    temporary_file.close()

                event._headers = scope["headers"]
                event._cookies = cookies
                if (register := self.register()) is None:
                    self.logger.error("Registration failed")
                    await send({
                        'type': 'http.response.start',
                        'status': 500,
                        'headers': self.get_default_headers(scope["headers"]),

                    })
                    return
                pipe, key = register
                event._key = key
                await loop.run_in_executor(None, self.ab_queue.put, event)
                available_data = await loop.run_in_executor(None, pipe.poll, REST_RESPONSE_TIMEOUT)
                if not available_data:
                    self.logger.error("No response was returned in %ss", REST_RESPONSE_TIMEOUT)
                    await send({
                        'type': 'http.response.start',
                        'status': 500,
                        'headers': self.get_default_headers(scope["headers"]),
                        'more_body': False

                    })
                    return

                event_response = pipe.recv()

                response = event_response.get_response()

                path = getattr(response, "path", None)
                if isinstance(path, Path):
                    headers = self.get_default_headers(scope["headers"], b"application/octet-stream")
                    headers.append((b"Content-Disposition", b'attachment; filename="' + response.name.encode("ascii",
                                                                                                             errors="ignore") + b'"; filename*=UTF-8\'\'' + quote(
                        response.name, safe="").encode()))
                    headers.append((b"Content-Length", str(path.lstat().st_size).encode()))
                    headers.append((b"Content-Type", response.content_type.encode()))
                    try:
                        with path.open("rb") as file:
                            await send({
                                'type': 'http.response.start',
                                'status': self.http_codes_mapping.get(response.get_status(), 500),
                                'headers': headers,
                            })
                            while True:
                                data = file.read(1024)
                                if not data:
                                    break
                                await send({
                                    'type': 'http.response.body',
                                    'body': data,
                                    'more_body': True
                                })

                            await send({
                                'type': 'http.response.body',
                                'body': b'',
                                'more_body': False
                            })
                    except FileNotFoundError:
                        self.logger.warning("File to download was not found: %s", path)
                        await send({
                            'type': 'http.response.start',
                            'status': 500,
                            'headers': headers,
                        })
                        await send({
                            'type': 'http.response.body',
                            'body': b'',
                            'more_body': False
                        })
                        return
                else:
                    await send({
                        'type': 'http.response.start',
                        'status': self.http_codes_mapping.get(response.get_status(), 500),
                        'headers': self.get_default_headers(scope["headers"]),

                    })

                    body = asdict(response, dict_factory=self.dict_factory)
                    body.update(response.dict)
                    body = {snake2camel(key): value for key, value in body.items() if not key.startswith("_")}

                    await send({
                        'type': 'http.response.body',
                        'body': dumps(body, ensure_ascii=False, cls=self.CustomJSONEncoder).encode("utf-8"),
                        'more_body': False
                    })

                self.unregister(pipe, key)

    def run(self) -> None:
        """
        Configures and starts the Uvicorn server to run the ASGI application for
        handling RESTful API requests.
        """
        config = Config(self.App(self.api_broker_queue), host="0.0.0.0", port=REST_PORT, log_level="debug", workers=8)
        # ssl_keyfile="/home/marek/rest.key",
        # ssl_certfile="/home/marek/rest.crt")
        server = Server(config)
        server.run()
