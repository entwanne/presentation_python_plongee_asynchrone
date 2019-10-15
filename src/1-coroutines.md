# Un monde de coroutines

## Coroutines

```python
async def simple_print(msg):
    print(msg)
```

```python
simple_print
```

```python
simple_print('Hello')
```

--------------------

```python
await simple_print('Hello')
```

--------------------

```python
coro = simple_print('Hello')
dir(coro)
```

```python
aw = coro.__await__()
aw
```

```python
dir(aw)
```

--------------------

```python
for _ in simple_print('Hello').__await__():
    pass
```

--------------------

```python
async def complex_work():
    await simple_print('Hello')
    await asyncio.sleep(0)
    await simple_print('World')


for _ in complex_work().__await__():
    pass
```

--------------------

```python
it = complex_work().__await__()
next(it)
```

```python
next(it)
```
