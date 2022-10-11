# For a Few Tools More

## Other tools

* Other tools to gain from async environment
* Other blocks: `async for` and `async with`

## Async iterables & generators

* An async iterable has an `__aiter__` method that returns an async iterator

--------------------

* The async iterator has an `__anext__` coroutine-method that returns the next element at each call

--------------------

* The method raises a `StopAsyncIteration` exception at the end of iteration


## Async iterables

* Example: async-equivalent to `range`

```python
class ARange:
    def __init__(self, stop):
        self.stop = stop

    def __aiter__(self):
        return ARangeIterator(self)


class ARangeIterator:
    def __init__(self, arange):
        self.arange = arange
        self.i = 0

    async def __anext__(self):
        if self.i >= self.arange.stop:
            raise StopAsyncIteration
        await sleep(1)
        i = self.i
        self.i += 1
        return i
```


## Async iterables

* Run inside our async engine

```python
async def test_for():
    async for val in ARange(5):
        print(val)

loop = Loop()
loop.run_task(test_for())
```


## Async generators

* In the same way we can define an async generator (Python 3.6)

```python
async def arange(stop):
    for i in range(stop):
        await sleep(1)
        yield i
```


## Async context managers

* Async context manager defined by its methods `__aenter__` and `__aexit__`

```python
class Server:
    def __init__(self, addr):
        self.socket = aiosocket()
        self.addr = addr

    async def __aenter__(self):
        await self.socket.bind(self.addr)
        await self.socket.listen()
        return self.socket

    async def __aexit__(self, *args):
        self.socket.close()
```


## Async context managers

* Run inside our async engine

```python
async def test_with():
    async with Server(('localhost', 8080)) as server:
        with await server.accept() as client:
            msg = await client.recv(1024)
            print('Received from client', msg)
            await client.send(msg[::-1])

loop = Loop()
loop.run_task(gather(test_with(), client_coro()))
```


## Async context managers

* Async context managers embedded in `contextlib` module (Python 3.7)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def server(addr):
    socket = aiosocket()
    try:
        await socket.bind(addr)
        await socket.listen()
        yield socket
    finally:
        socket.close()
```
