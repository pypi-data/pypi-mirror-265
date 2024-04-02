from asyncio import Event, get_event_loop, create_task, wait, AbstractEventLoop
from json import dumps, loads
from multiprocessing import Process, Queue
from typing import Optional

from websockets import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from dataclasses import asdict

from edri.abstract.api_base import APIBase
from edri.config.constant import ApiType
from edri.config.setting import HOST, WS_PORT
from edri.dataclass.event import api_events
from edri.dataclass.event.response import ResponseStatus
from edri.utility.function import snake2camel


class API(APIBase, Process):

    def __init__(self, ab_queue: "Queue[Event]") -> None:
        super().__init__(ab_queue)
        self.event_loop: Optional[AbstractEventLoop] = None
        self.events = {event.resource: event.event for event in api_events if ApiType.WS not in event.exclude}
        self.commands = {event.event: event.resource for event in api_events if ApiType.WS not in event.exclude}

    @property
    def name(self) -> str:
        return "Websocket API"

    @property
    def type(self) -> ApiType:
        return ApiType.WS

    async def new_client(self, websocket: WebSocketServerProtocol, url) -> None:
        self.logger.debug("New connection: %s %s", websocket.remote_address[0], url)
        for middleware in self.middlewares:
            if not middleware.process_req(websocket, url):
                return
        if (register := self.register()) is None:
            return
        client_pipe, key = register
        frame_available = Event()
        self.event_loop.add_reader(client_pipe.fileno(), frame_available.set)
        from_core = create_task(frame_available.wait())
        from_client = create_task(websocket.recv())
        tasks = {from_core, from_client}
        while True:
            try:
                done, pending = await wait(tasks, return_when="FIRST_COMPLETED")
                tasks = set()
                for task in done:
                    if task == from_core:
                        event = client_pipe.recv()
                        self.logger.debug(f"<- API Broker %s %s", key, event)
                        data = {
                            "command": self.commands[event.__class__]
                        }
                        data.update(asdict(event))
                        data.pop("_key")
                        data.pop("_switch")
                        data.pop("_stream")
                        data.pop("method", None)
                        if data["response"]:
                            status = data["response"].pop("_status")
                            data["response"]["event_status"] = status.value
                            data["response"].pop("_error")
                            data["response"].pop("_changed")
                            data["response"] = {snake2camel(key): value for key, value in data["response"].items() if not key.startswith("_")}
                        else:
                            data.pop("response")
                        await self.event_loop.create_task(websocket.send(dumps(data)))

                        from_core.cancel()
                        frame_available = Event()
                        self.event_loop.add_reader(client_pipe.fileno(), frame_available.set)
                        from_core = create_task(frame_available.wait())
                        tasks.add(from_core)
                    elif task == from_client:
                        ws_event: str = task.result()
                        self.logger.debug(f"-> %s %s", key, ws_event)
                        try:
                            ws_event = loads(ws_event)
                        except Exception as e:
                            await self.event_loop.create_task(
                                websocket.send(dumps(["Warning", {"warning": "Malformed JSON"}])))
                            self.logger.warning("Malformed JSON: %s", ws_event, exc_info=e)
                        else:
                            if not isinstance(ws_event, dict) or "command" not in ws_event:
                                await self.event_loop.create_task(
                                    websocket.send(dumps(ws_event)))
                                self.logger.warning("Unknown data: %s", ws_event)
                            else:
                                command = ws_event.pop("command")
                                if (event_type := self.events.get(command, None)) is None:
                                    ws_event["command"] = command
                                    ws_event["response"] = {
                                        "status": ResponseStatus.FAILED.value,
                                        "reason": "Unknown command"
                                    }
                                    await self.event_loop.create_task(
                                        websocket.send(dumps(ws_event)))
                                    self.logger.warning("Unknown command: %s", command)
                                else:
                                    try:
                                        event = event_type(**ws_event)
                                    except Exception as e:
                                        self.logger.warning("Cannot instantiated event: %s", command, exc_info=e)
                                        return
                                    event._key = key
                                    self.ab_queue.put(event)

                        finally:
                            from_client.cancel()
                            from_client = create_task(websocket.recv())
                            tasks.add(from_client)
                tasks = tasks | pending
                if len(tasks) == 0:
                    break

            except ConnectionClosedError as e:
                from_core.cancel()
                from_client.cancel()
                self.logger.info("ConnectionClosedError: %s", key, exc_info=e)
                break

            except ConnectionClosedOK as e:
                from_core.cancel()
                from_client.cancel()
                self.logger.debug("ConnectionClosedOK: %s", key, exc_info=e)
                break

            except ValueError as e:
                from_core.cancel()
                from_client.cancel()
                self.logger.warning("ValueError: %s", key, exc_info=e)
                break

        self.event_loop.remove_reader(client_pipe.fileno())
        self.unregister(client_pipe, key)
        return

    def run(self) -> None:
        self.event_loop = get_event_loop()
        start_server = serve(self.new_client, HOST, WS_PORT)

        self.event_loop.run_until_complete(start_server)
        self.logger.info("WebSocket API has started!")
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            return
