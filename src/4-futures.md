# Futures

## Futures

* L'implémentation précédente de `sleep` est inefficace
* La tâche est sans cesse reprogrammée pour rien
* De même pour la tâche `Waiter` qui n'a besoin d'être lancée qu'une fois sa condition validée

--------------------

* `asyncio` utilise un mécanisme de _futures_ :

```python
async def test():
    await asyncio.sleep(1)

loop = Loop()
loop.run_task(test())
```

* Le `yield` utilisé pour rendre la main à la boucle peut être accompagné d'une valeur

--------------------

* _Future_ n'ayant pour but d'être reprogrammé qu'une fois sa condition validée

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

* Détection des _futures_ par la boucle événementielle

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

* Prise en compte des événements temporels
* Ajout d'une méthode `call_later`

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
