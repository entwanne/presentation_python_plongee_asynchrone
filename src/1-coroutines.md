# A world of coroutines


## Coroutines

* Definition of a coroutine since Python 3.5 :

```python
async def simple_print(msg):
    print(msg)
```

--------------------

* `simple_print` is a function that returns a coroutine

```python
simple_print
```

```python
simple_print('Hello')
```


## Coroutines

* The body is executed by the async engine, here with `await` keyword

```python
await simple_print('Hello')
```

--------------------

* Outside of an async *REPL* we would use `asyncio.run`

```python
asyncio.run(simple_print('Hello'))
```

* Or directly interact with the event loop:

```python
loop = asyncio.new_event_loop()
loop.run_until_complete(simple_print('Hello'))
```

--------------------

* This loop executes and schedules the different tasks
* It allows concurrent execution


## Coroutines - introspection

* What is a coroutine?

--------------------

* It's an object with an `__await__` method

```python
coro = simple_print('Hello')
dir(coro)
```


## Coroutines - introspection

* This method returns an iterator (`coroutine_wrapper`)

```python
aw = coro.__await__()
aw
```

```python
dir(aw)
```


## Coroutines - iteration

* We can iterate manually over a coroutine

```python
for _ in simple_print('Hello').__await__():
    pass
```


## Coroutines - iteration

* Even with a more complex coroutine

```python
async def complex_work():
    await simple_print('Hello')
    await asyncio.sleep(0)
    await simple_print('World')


for _ in complex_work().__await__():
    pass
```


## Coroutines - iteration

* Our loop runs multiple iterations

```python
it = complex_work().__await__()
next(it)
```

```python
next(it)
```

--------------------

* The loop takes control back after each iteration
* `await asyncio.sleep(0)` is similar to a `yield` in a generator (suspend)
* `await` is equivalent to `yield from`
