# Attendez-moi !

## Awaitables

```python
class ComplexWork:
    def __await__(self):
        print('Hello')
        yield
        print('World')
```

```python
await ComplexWork()
```

--------------------

```python
it = ComplexWork().__await__()
next(it)
```

```python
next(it)
```

```python
class Waiter:
    def __init__(self):
        self.done = False

    def __await__(self):
        while not self.done:
            yield
```

--------------------

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
