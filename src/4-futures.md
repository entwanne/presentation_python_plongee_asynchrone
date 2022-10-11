# No Future


## Futures

* The previous implementation of `sleep` function is unefficient
* The task is continously rescheduled for nothing
* Same for the `Waiter` task that could be run only when its condition is true


## Futures - asyncio

* `asyncio` uses _futures_ for that:

```python
async def test():
    await asyncio.sleep(1)

loop = Loop()
loop.run_task(test())
```

--------------------

* `yield` keyword used to give control to the loop could take an argument


## Futures - example

* This _future_ should only be rescheduled once its condition is validated

```python
class Future:
    def __await__(self):
        yield self
        assert self.done
```


## Futures - example

* We add a validation method to reschedule the task

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


## Futures - event loop

* The event loop detects _futures_ objects

```python
class Loop:
    [...]

    def run(self):
        Loop.current = self
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                result = next(task)
            except StopIteration:
                continue

            if isinstance(result, Future):
                result.task = task
            else:
                self.tasks.append(task)
```


## Futures - time events

* We want to link a _future_ with a clock time
* For that we add an handler for time events

```python
from functools import total_ordering

@total_ordering
class TimeEvent:
    def __init__(self, t, future):
        self.t = t
        self.future = future

    def __eq__(self, rhs):
        return self.t == rhs.t

    def __lt__(self, rhs):
        return self.t < rhs
```


## Futures - time events

* We add a `call_later` method to the loop class

```python
import heapq

class Loop:
    [...]

    handlers = []

    def call_later(self, t, future):
        heapq.heappush(self.handlers, TimeEvent(t, future))
```


## Futures - time events

* And we handle time events in the event loop

```python
class Loop:
    [...]

    def run(self):
        Loop.current = self
        while self.tasks or self.handlers:
            if self.handlers and self.handlers[0].t <= time.time():
                handler = heapq.heappop(self.handlers)
                handler.future.set()

            if not self.tasks:
                continue
            task = self.tasks.pop(0)
            try:
                result = next(task)
            except StopIteration:
                continue

            if isinstance(result, Future):
                result.task = task
            else:
                self.tasks.append(task)
```


## Futures - utils

* Now we can write a better version for `sleep` function

```python
import time

async def sleep(t):
    future = Future()
    Loop.current.call_later(time.time() + t, future)
    await future
```

```python
async def foo():
    print('before')
    await sleep(5)
    print('after')
```

```python
loop = Loop()
loop.run_task(foo())
```
