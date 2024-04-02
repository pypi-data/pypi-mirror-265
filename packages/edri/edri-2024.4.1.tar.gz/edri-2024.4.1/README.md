# EDRI Event Driven Routing Infrastructure

> ## Origin and intention
> The original idea of this project was to offer users a simplified way to create applications that make good use of parallelism -
> running code across multiple threads or processes or even another machines.
> ### Event Driven
> Everything that individual workers need to perform must be controlled and managed in some way.
> In this case, events serve this purpose events physically represent messages that are forwarded between different elements.
> ### Routing Infrastructure
> The exchange and delivery of events are ensured similarly to computer networks TCP/IP.
> In this case, however, networks (IP ranges) are replaced with types of events, such as file upload.
> The router must know to whom each event is intended.

## Architecture

The internal architecture of this framework is built on several types of elements.
The most important element and the focal point of every project built on this framework is the *router*.
Furthermore, we encounter managers and workers. To interconnect multiple routers, a network terminology element named switch is used.
Lastly, there are several specially modified managers, see below.

![Basic](docs/basic.svg)

### Events

Events physically represent messages data packets. These data packets are created
using [data classes](https://docs.python.org/3/library/dataclasses.html).
The most important piece of information is carried by the event in the form of its type, while the event is an instance of a data class.
Each event can exist in two states depending on whether it contains a response or not.
**Each event can have multiple recipients as well as multiple senders.**
All events must be strictly defined.

#### Types of Events

    ##### Notification
      This type of event serves to announce that some event has occurred. A response is not expected.
      For example, a notification can be sent to announce that a new file has been uploaded.

    ##### Request
      This type of event is used to obtain some information.
      The concerned manager is expected to ensure the acquisition of the requested information.
      This information will be added to the event as a response and sent.
      For example, it can be a user's query via API to get a list of files.

     ##### Tunnel
       A special type of events that serves to ensure continuous exchange of information between workers.
       A tunnel must first be established and confirmed by both parties of the conversation.
       For example, if one worker needs to convert data to another format,
       it can establish a tunnel with a worker that has this functionality implemented.
       The transfer of data, both source and resulting, can occur quantitatively,
       i.e., in individual parts that can be processed independently.

### Router

The central element that serves to forward events. This element ensures the exchange of events between the framework's elements -
typically managers.
It can also be the only element, which can be connected to the switch using a connector, this connection is made via a TCP/IP socket, thus
it is possible to parallelize tasks on multiple computing nodes.
Connection to the switch is cached, so short-term (within tens of seconds) network outages do not pose a problem.

### Manager

An element serving to distribute tasks contained in the transmitted events to individual workers.
The manager automatically supports running three types of tasks as functions, threads, and processes.
The manager is also the element that ensures the transfer of data for individual tunnels.
The manager must inform the router of all types of messages it would like to receive.
In essence, it must subscribe to their delivery.

#### Types of Tasks

##### Function

Runs in the manager itself. Suitable only for very fast tasks. The manager cannot perform any other activity meanwhile.

##### Thread

The function will be run in a new thread.
Parallelization depends on the interpreter.
Parallelization typically occurs only when the program runs outside the Python interpreter,
see [GIL](https://wiki.python.org/moin/GlobalInterpreterLock).

##### Process

The function will be run in a new process.
The most resource-intensive method, but it offers full task parallelization by running in a separate process.

#### Message Priority

The manager offers two approaches.

##### FIFO

Messages are processed as they are received.

##### Priority FIFO

Messages are processed according to the specified priority lower means higher precedence.
Messages with the same priority are processed as FIFO.

#### Special Managers

##### Scheduler

A special manager used for time-defined event sending.
An example could be backup during night hours.

##### Key-Value Store

A special manager that allows the use of a built-in key-value store.
For example, after starting data download, the data are cached using the store and periodically updated by the scheduler.

##### API Broker

A special manager used to merge all APIs from the external world outside.

###### REST

An API that implements the REST protocol. Messages are converted into request-type events based on URL addresses.
Responses are then passed on to clients. This API allows only the use of request-type events.

###### WebSocket

An API that implements the WebSocket protocol. Messages are converted into events based on schemas.
Responses, as with REST, are passed on to users, however, the connection is not terminated.
Thanks to this feature, the API allows sending not only request-type events but also notification-type events, both ways.

### Worker

A function/class defined by the programmer serving to perform a task.

### Switch connector

A special type of element that ensures the connection between the router and the switch.
It takes care of bridging the traffic between internal inter-processor communication and TCP/IP connection.
Furthermore, it ensures the distribution of routed messages to other routers and vice versa.
Last but not least, it takes care of ensuring the continuity of sent messages -
so that no message is omitted or sent multiple times in case of a connection interruption.

## Usage

### Launching

```python

if __name__ == "__main__":
    from edri import EDRI

    edri = EDRI()
    edri.run()
```

### Creating a Manager

The simplest example of implementing a manager named 'DummyManager' without any subscribed events.

```python
from edri.abstract import ManagerBase


class DummyManager(ManagerBase):
    pass
```

### Subscribing to Message Delivery

Subscribing to the test event Ping as a request (without response) would look like this.
Functions must be named according to the following schema: solve_(req|res)_<anything>, e.g., solve_req_ping.
Furthermore, the function must contain a parameter for the instance object typically Self, and another parameter must be named event,
its data type is not only mandatory but functionally necessary because it defines which event will be mapped for this function.

```python   
from edri.events.edri.test import Ping
from edri.abstract import ManagerBase

class DummyManager(ManagerBase):
    def solve_req_ping(self, event: Ping) -> None:
        ...
```

### How to Launch a Thread/Process

The first thing is the need to create the thread/process class itself.
Creating a class is the only moment when the way to create a new thread differs from that of a process.
For proper operation, it's necessary to create a subclass from `from .abstract.worker import WorkerThread` in the case of a thread,
or similarly `from edri.abstract.worker import WorkerProcess` for a process.
The `do` function replaces the usual `run` function you might be familiar with from standard Python libraries.
For better typing, the message type that the worker was launched with can be passed as a generic type.

```python
from edri.abstract.worker import WorkerProcess
from edri.events.edri.test import Ping


class Worker(WorkerProcess[Ping]):
    def do(self) -> None:
        ...
```

### Scheduler

The scheduler is used for scheduled sending of events.
The scheduler is not meant for inheritance; initial messages can be inserted as parameters at its launch.
One of the disadvantages of such created tasks is the inability to set their name.
Generally, it's recommended to create tasks dynamically, e.g., in the after_start() function of any manager,
this way, the task's name can also be set, which can then be used for its cancellation.

```python
from datetime import timedelta, datetime
from edri.utility.scheduler import Job
from edri.events.edri.test import Ping

if __name__ == "__main__":
    from edri import EDRI

    jobs = [
        Job(event=Ping(),
            when=datetime.now(),
            repeat=timedelta(seconds=1))
    ]
    edri = EDRI()
    edri.start_scheduler(jobs)
    edri.run()
```

### Key-Value Store

Used for data sharing. The most common use is the ability to insert data in one manager and read data from another manager.
For example, periodic downloading of data from the internet and caching it using the Key-Value Store. Another manager can use these data meanwhile without interruption.
To maintain stateless operation of individual functions, it's possible to send request data, which will be returned along with the response.

Processing a response from the Key-Value Store could look like this.
It's important to realize that this function **will receive other events besides the requested ones.**

```python
from edri.events.edri.store import Get
from edri.events.edri.router import HealthCheck
from edri.abstract import ManagerBase

class DummyManager(ManagerBase):
    def solve_req_requiring_data_from_kv_store(self, event: HealthCheck) -> None:
        store_get = Get(name="key_of_data", data=event)
        self.router_queue.put(store_get)


    def solve_res_store_get(self, event: Get) -> None:
        if event.name == "key_of_data" and event.data.__class__ == HealthCheck:
            ...
```

Setting the value is then straightforward.

```python
from edri.events.edri.store import Set
from edri.events.edri.router import HealthCheck
from edri.abstract import ManagerBase

class DummyManager(ManagerBase):
    def solve_health_check(self, message: HealthCheck) -> None:
        store_set = Set(name="health_check", value="I'm fine")
        self.router_queue.put(store_set)
```

### API

#### REST

### Events

#### Creation

Creating an event equals instantiating the event class.

```python
from edri.events.edri.test import Ping

ping = Ping()
```

#### Response

Setting the response can be divided into two levels, just the status code or data.
In the case of filling in data, the status code is automatically set to "OK".
It's not necessary to send the response; setting the status or any data
will automatically send it after the function finishes.

Just the status code:

```python
from edri.events.edri.test import Ping
from edri.dataclass.event.response import ResponseStatus

ping = Ping()
ping.response.set_status(ResponseStatus.OK)
```

Just the response data:

```python
from edri.events.edri.test import Test

test = Test()
test.response.random = 1234
```

#### Sending a Message

Sending a message is done differently in a manager and a worker.

##### Manager

In the manager, messages are inserted directly into the router queue.

```python
from edri.abstract import ManagerBase
from edri.events.edri.test import Ping, Test


class DummyManager(ManagerBase):
    def solve_req_do_something(self, event: Test) -> None:
        ping = Ping()
        self.router_queue.put(ping)
```

##### Worker

The worker class has its own function for sending messages

```python
from edri.abstract.worker import WorkerProcess
from edri.events.edri.test import Ping


class Worker(WorkerProcess):
    def do(self) -> None:
        ping = Ping()
        self.message_send(ping)
```