# Futures

## Futures

```python
async def test():
    await asyncio.sleep(1)

loop = Loop()
loop.run_task(test())
```

--------------------

```python
class Future:
    def __await__(self):
        yield self
        assert self.done
```

--------------------

```python
class Future:
    def __init__(self):
        self._done = False
        self.task = None

    def __await__(self):
        yield self
        assert self._done

    def set(self):
        self._done = True
        if self.task is not None:
            Loop.current.add_task(self.task)
```

--------------------

```python
class Loop:
    ...

    def run(self):
        ...
        if isinstance(result, Future):
            result.task = task
        else:
            self.tasks.append(task)
```

--------------------

```python
@total_ordering
class TimeEvent:
    def __init__(self, t, future):
        self.t = t
        self.future = future
    def __eq__(self, rhs):
        return self.t == rhs.t
    def __lt__(self, rhs):
        return self.t < rhs

class Loop:
    ...
    def call_later(self, t, future):
        heapq.push(self.handlers, TimeEvent(t, future))

    def run(self):
        ...
        if self.handlers and self.handlers[0].t <= time.time():
            handler = heapq.pop(self.handlers)
            handler.future.set()
        ...
```
