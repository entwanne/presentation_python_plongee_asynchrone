# Quelques autres outils

## Autres outils

* Nouveaux outils pour profiter de l'environnement asynchrone
* Nouveaux blocs : `for` et `with` asynchrones (`async for`, `async with`)

## Itérables et générateurs asynchrones

* Un intérable asynchrone possède une méthode `__aiter__` renvoyant un itérateur asynchrone
* L'itérateur asynchrone a une méthode-coroutine `__anext__` renvoyant le prochain élément
* La méthode lève une exception `StopAsyncIteration` en fin d'itération

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

* Exécution au sein de notre moteur asynchrone

```python
async def test_for():
    async for val in ARange(5):
        print(val)

loop = Loop()
loop.run_task(test_for())
```

--------------------

* On peut de façon similaire définir un générateur asynchrone (Python 3.6)

```python
async def arange(stop):
    for i in range(stop):
        await sleep(1)
        yield i
```

## Gestionnaires de contexte asynchrones

* Contexte asynchrone défini par ses méthodes `__aenter__` et `__aexit__`

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

* Contextes asynchrones intégrés à la `contextlib` (Python 3.7)

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
