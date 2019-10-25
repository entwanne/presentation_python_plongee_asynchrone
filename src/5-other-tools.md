# Et pour quelques outils de plus

## Autres outils

* Nouveaux outils pour profiter de l'environnement asynchrone
* Nouveaux blocs : `for` et `with` asynchrones (`async for`, `async with`)

## Itérables et générateurs asynchrones

* Un itérable asynchrone possède une méthode `__aiter__` renvoyant un itérateur asynchrone
* L'itérateur asynchrone a une méthode-coroutine `__anext__` renvoyant le prochain élément
* La méthode lève une exception `StopAsyncIteration` en fin d'itération


## Itérables asynchrones

* Exemple : équivalent asychrone à `range`

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


## Itérables asynchrones

* Exécution au sein de notre moteur asynchrone

```python
async def test_for():
    async for val in ARange(5):
        print(val)

loop = Loop()
loop.run_task(test_for())
```


## Générateurs asynchrones

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


## Gestionnaires de contexte asynchrones

* Exécution au sein de notre moteur asynchrone

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


## Gestionnaires de contexte asynchrones

* Contextes asynchrones intégrés à la `contextlib` (Python 3.7)

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
