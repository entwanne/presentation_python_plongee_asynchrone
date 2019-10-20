# Attendez-moi !


## Awaitables

* Les coroutines sont des tâches asynchrones (*awaitables*)
* Un awaitable est un objet avec une méthode `__await__`

* Tâche équivalente à la coroutine `complex_work` :

```python
class ComplexWork:
    def __await__(self):
        print('Hello')
        yield
        print('World')
```

* Le `yield` rend la méthode génératrice, qui renvoie donc un itérateur

```python
await ComplexWork()
```


## Awaitables - itération

* Itération manuelle sur notre tâche

```python
it = ComplexWork().__await__()
next(it)
```

```python
next(it)
```


## Awaitables

* Les tâches autres que les coroutines sont peu courantes
* Utiles pour conserver un état associé à la tâche

```python
class Waiter:
    def __init__(self):
        self.done = False

    def __await__(self):
        while not self.done:
            yield
```


## Awaitables - synchronisation

* Permet à deux tâches de se synchroniser

```python
waiter = Waiter()

async def wait_job(waiter):
    print('start')
    await waiter # wait for count_up_to to be finished
    print('finished')

async def count_up_to(waiter, n):
    for i in range(n):
        print(i)
        await asyncio.sleep(0)
    waiter.done = True

await asyncio.gather(wait_job(waiter), count_up_to(waiter, 10))
```
