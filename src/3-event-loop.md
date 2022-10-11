# Goldilocks and the three tasks


## Event loops

* First prototype of an event loop

```python
def run_task(task):
    it = task.__await__()

    while True:
        try:
            next(it)
        except StopIteration:
            break
```


## Event loops

* Not really useful if it executes only one task
* Better version to schedule multiple tasks
* Use a queue to know the next task to iterate over

```python
def run_tasks(*tasks):
    tasks = [task.__await__() for task in tasks]

    while tasks:
        # We take the first available task
        task = tasks.pop(0)
        try:
            next(task)
        except StopIteration:
            # Task is over
            pass
        else:
            # Task is not finished, we enqueue it to continue it later
            tasks.append(task)
```


## Event loops - execution

* Some examples of concurrent execution

```python
run_tasks(simple_print(1), ComplexWork(), simple_print(2), simple_print(3))
```

```python
waiter = Waiter()
run_tasks(wait_job(waiter), count_up_to(waiter, 5))
```


## Asynchronous environment

* Unit task to give control back to the event loop

```python
class interrupt:
    def __await__(self):
        yield
```

--------------------

* That let us write some helpers

```python
import time

async def sleep_until(t):
    while time.time() < t:
        await interrupt()

async def sleep(duration):
    await sleep_until(time.time() + duration)
```


## Asynchronous environment - example

* And use them in our envirionment

```python
async def print_messages(*messages, sleep_time=1):
    for msg in messages:
        print(msg)
        await sleep(sleep_time)
```

```python
run_tasks(print_messages('foo', 'bar', 'baz'),
    print_messages('aaa', 'bbb', 'ccc', sleep_time=0.7))
```


## Event loops - interactions

* An event loop is more useful if we can interact with it once run
* Prototype of a new loop that can schedule new tasks on the fly (`add_task`)

```python
class Loop:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if hasattr(task, '__await__'):
            task = task.__await__()
        self.tasks.append(task)

    def run(self):
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.add_task(task)
```


## Event loops - interactions

* New method to easily run a task

```python
class Loop:
    [...]

    def run_task(self, task):
        self.add_task(task)
        self.run()
```

```python
loop = Loop()
loop.run_task(print_messages('foo', 'bar', 'baz'))
```


## Event loops - interactions

* Adding `Loop.current` classvar to make the loop reachable from tasks

```python
class Loop:
    [...]

    current = None

    def run(self):
        Loop.current = self
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.add_task(task)
```


## Event loops - utility functions

* `gather` implementation to wait for multiple tasks simultaneously

* Better `Waiter` class to wait for multiple checks

```python
class Waiter:
    def __init__(self, n=1):
        self.i = n

    def set(self):
        self.i -= 1

    def __await__(self):
        while self.i > 0:
            yield
```


## Event loops - utility functions

* Used by `gather` to wait for `N` tasks

```python
async def gather(*tasks):
    waiter = Waiter(len(tasks))

    async def task_wrapper(task):
        await task
        waiter.set()

    for t in tasks:
        Loop.current.add_task(task_wrapper(t))
    await waiter
```

```python
loop = Loop()
loop.run_task(gather(print_messages('foo', 'bar', 'baz'),
    print_messages('aaa', 'bbb', 'ccc', sleep_time=0.7)))
```


## Event loops - network utils

* Other functions: handling async sockets
* Use `select` to know when the socket is available
* Go back to the event loop when unavailable


## Event loops - network utils

```python
import select

class AIOSocket:
    def __init__(self, socket):
        self.socket = socket
        self.pollin = select.epoll()
        self.pollin.register(self, select.EPOLLIN)
        self.pollout = select.epoll()
        self.pollout.register(self, select.EPOLLOUT)

    def close(self):
        self.socket.close()

    def fileno(self):
        return self.socket.fileno()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.socket.close()
```


## Event loops - network utils

```python
class AIOSocket:
    [...]

    async def bind(self, addr):
        while not self.pollin.poll():
            await interrupt()
        self.socket.bind(addr)

    async def listen(self):
        while not self.pollin.poll():
            await interrupt()
        self.socket.listen()

    async def connect(self, addr):
        while not self.pollin.poll():
            await interrupt()
        self.socket.connect(addr)
```


## Event loops - network utils

```python
class AIOSocket:
    [...]

    async def accept(self):
        while not self.pollin.poll(0):
            await interrupt()
        client, _ = self.socket.accept()
        return self.__class__(client)

    async def recv(self, bufsize):
        while not self.pollin.poll(0):
            await interrupt()
        return self.socket.recv(bufsize)

    async def send(self, bytes):
        while not self.pollout.poll(0):
            await interrupt()
        return self.socket.send(bytes)
```


## Event loops - network utils

```python
import socket

def aiosocket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
    return AIOSocket(socket.socket(family, type, proto, fileno))
```


## Event loops - network utils

```python
async def server_coro():
    with aiosocket() as server:
        await server.bind(('localhost', 8080))
        await server.listen()
        with await server.accept() as client:
            msg = await client.recv(1024)
            print('Received from client', msg)
            await client.send(msg[::-1])

async def client_coro():
    with aiosocket() as client:
        await client.connect(('localhost', 8080))
        await client.send(b'Hello World!')
        msg = await client.recv(1024)
        print('Received from server', msg)

loop = Loop()
loop.run_task(gather(server_coro(), client_coro()))
```
