# Un monde de coroutines


## Coroutines

* Définition d'une coroutine depuis Python 3.5 :

```python
async def simple_print(msg):
    print(msg)
```

* `simple_print` est une fonction renvoyant une coroutine

```python
simple_print
```

```python
simple_print('Hello')
```


## Coroutines

* Le contenu est exécuté par le moteur asynchrone, ici à l'aide d'`await`

```python
await simple_print('Hello')
```

* En dehors d'un *REPL* asynchrone, il faudrait utiliser `asyncio.run`

```python
asyncio.run(simple_print('Hello'))
```

* Ou encore interagir directement avec la boucle événementielle :

```python
loop = asyncio.new_event_loop()
loop.run_until_complete(simple_print('Hello'))
```

* Cette boucle exécute et cadence les différentes tâches
* Elle permet une utilisation concurrente


## Coroutines - introspection

* De quoi est faite une coroutine ?
* C'est un objet avec une méthode `__await__`

```python
coro = simple_print('Hello')
dir(coro)
```


## Coroutines - introspection

* Cette méthode renvoie un itérateur (`coroutine_wrapper`)

```python
aw = coro.__await__()
aw
```

```python
dir(aw)
```


## Coroutines - itération

* On peut donc itérer manuellement sur une coroutine

```python
for _ in simple_print('Hello').__await__():
    pass
```


## Coroutines - itération

* De même avec une coroutine plus complexe

```python
async def complex_work():
    await simple_print('Hello')
    await asyncio.sleep(0)
    await simple_print('World')


for _ in complex_work().__await__():
    pass
```


## Coroutines - itération

* Plusieurs itérations sont bien parcourues

```python
it = complex_work().__await__()
next(it)
```

```python
next(it)
```

* La boucle reprend le contrôle à chaque interruption
* Le `await asyncio.sleep(0)` a pour effet de `yield`
* `await` est équivalent à `yield from`
