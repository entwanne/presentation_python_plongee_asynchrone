# No Future


## Futures

* L'implémentation précédente de `sleep` est inefficace
* La tâche est sans cesse reprogrammée pour rien
* De même pour la tâche `Waiter` qui n'a besoin d'être lancée qu'une fois sa condition validée


## Futures - asyncio

* `asyncio` utilise un mécanisme de _futures_ :

```python
async def test():
    await asyncio.sleep(1)

loop = Loop()
loop.run_task(test())
```

--------------------

* Le `yield` utilisé pour rendre la main à la boucle peut être accompagné d'une valeur


## Futures - exemple

* Cette _future_ ne doit être relancée qu'une fois sa condition validée

```python
class Future:
    def __await__(self):
        yield self
        assert self.done
```


## Futures - exemple

* On ajoute une méthode de validation qui reprogramme la tâche

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


## Futures - boucle événementielle

* Détection des _futures_ par la boucle événementielle

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


## Futures - événements temporels

* L'idée est d'associer une _future_ à un temps
* On intègre pour cela une gestion d'événéments temporels

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


## Futures - événements temporels

* Ajout d'une méthode `call_later`

```python
import heapq

class Loop:
    [...]

    handlers = []

    def call_later(self, t, future):
        heapq.heappush(self.handlers, TimeEvent(t, future))
```


## Futures - événements temporels

* Prise en compte des événements temporels par la boucle

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


## Futures - utilitaires

* Ce qui nous permet une meilleure version de `sleep`

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
