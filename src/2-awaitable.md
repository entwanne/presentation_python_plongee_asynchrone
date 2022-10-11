# Wait for me!


## Awaitables

* Coroutines are asynchronous tasks (*awaitables*)
* An awaitable is an object with an `__await__` method

--------------------

* Async task equivalent to `complex_work` coroutine:

```python
class ComplexWork:
    def __await__(self):
        print('Hello')
        yield
        print('World')
```

* `yield` makes this method a generator-function, that returns then a generator

```python
await ComplexWork()
```


## Awaitables - iteration

* Our task fits with the previous protocol

```python
it = ComplexWork().__await__()
next(it)
```

```python
next(it)
```


## Awaitables

* Tasks other than coroutines are rare
* But they are useful to save a state linked to this task

```python
class Waiter:
    def __init__(self):
        self.done = False

    def __await__(self):
        while not self.done:
            yield
```


## Awaitables - synchronization

* `Waiter` let you synchronize two tasks

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
