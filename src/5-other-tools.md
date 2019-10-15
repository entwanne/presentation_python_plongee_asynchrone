# Quelques autres outils

## Autres outils

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

--------------------

```python
async def test_for():
    async for val in ARange(5):
        print(val)

loop = Loop()
loop.run_task(test_for())
```

--------------------

```python
async def arange(stop):
    for i in range(stop):
        await sleep(1)
        yield i
```

--------------------

```python
class SQL:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        await self.conn.connect()
        return self.conn

    async def __aexit__(self, *args):
        await self.conn.close()
```

--------------------

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def sql():
    try:
        print('Connecting...')
        await sleep(1)
        yield
    finally:
        print('Closing')
        await sleep(1)
```
