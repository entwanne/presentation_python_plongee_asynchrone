# Boucles événementielles


## Boucles événementielles

* Premier prototype de boucle événementielle

```python
def run_task(task):
    it = task.__await__()

    while True:
        try:
            next(it)
        except StopIteration:
            break
```


## Boucles évenementielles

* Peu d'utilité pour n'exécuter qu'une seule tâche
* Version améliorée pouvant cadencer plusieurs tâches
* Utilisation d'une file pour connaître la prochaîne tâche à itérer

```python
def run_tasks(*tasks):
    tasks = [task.__await__() for task in tasks]

    while tasks:
        # On prend la première tâche disponible
        task = tasks.pop(0)
        try:
            next(task)
        except StopIteration:
            # La tâche est terminée
            pass
        else:
            # La tâche continue, on la remet en queue de liste
            tasks.append(task)
```


## Boucles évenementielles - exécution

* Quelques exemples d'exécution concurrente

```python
run_tasks(simple_print(1), ComplexWork(), simple_print(2), simple_print(3))
```

```python
waiter = Waiter()
run_tasks(wait_job(waiter), count_up_to(waiter, 5))
```


## Environnement asynchrone

* Tâche unitaire simple pour rendre la main à la boucle

```python
class interrupt:
    def __await__(self):
        yield
```

* Qui nous permet de développer d'autres utilitaires

```python
import time

async def sleep_until(t):
    while time.time() < t:
        await interrupt()

async def sleep(duration):
    await sleep_until(time.time() + duration)
```


## Environnement asynchrone - exemple

* Et d'en profiter dans notre environnement

```python
async def print_messages(*messages, sleep_time=1):
    for msg in messages:
        print(msg)
        await sleep(sleep_time)
```

```python
run_tasks(print_messages('foo', 'bar', 'baz'),
    print_messages('aaa', 'bbb', 'ccc', sleep_time=0.7))
```


## Boucles événementielles - interactions

* Une boucle événementielle est plus utile si nous pouvons interagir avec elle une fois lancée
* Prototype d'une nouvelle boucle pouvant programmer des tâches à la volée (`add_task`)

```python
class Loop:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if hasattr(task, '__await__'):
            task = task.__await__()
        self.tasks.append(task)

    def run(self):
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.add_task(task)
```


## Boucles événementielles - interactions

* Ajout d'une méthode pour faciliter le lancement

```python
class Loop:
    [...]

    def run_task(self, task):
        self.add_task(task)
        self.run()
```

```python
loop = Loop()
loop.run_task(print_messages('foo', 'bar', 'baz'))
```


## Boucles événementielles - interactions

* Ajout de `Loop.current` pour rendre la boucle accessible depuis nos tâches

```python
class Loop:
    [...]

    current = None

    def run(self):
        Loop.current = self
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.add_task(task)
```


## Boucles événementielles - utilitaires

* Implémentation de `gather`, utilitaire permettant d'attendre simultanément plusieurs tâches

* Amélioration de notre classe `Waiter` pour attendre plusieurs validations

```python
class Waiter:
    def __init__(self, n=1):
        self.i = n

    def set(self):
        self.i -= 1

    def __await__(self):
        while self.i > 0:
            yield
```


## Boucles événementielles - utilitaires

* Utilisée par `gather` pour attendre `N` tâches

```python
async def gather(*tasks):
    waiter = Waiter(len(tasks))

    async def task_wrapper(task):
        await task
        waiter.set()

    for t in tasks:
        Loop.current.add_task(task_wrapper(t))
    await waiter
```

```python
loop = Loop()
loop.run_task(gather(print_messages('foo', 'bar', 'baz'),
    print_messages('aaa', 'bbb', 'ccc', sleep_time=0.7)))
```


## Boucles événementielles - utilitaires

* Autre utilitaire : gestion de _sockets_ asynchrones
* Utilisation de `select` pour savoir quand la _socket_ est disponible
* Renvoi à la boucle événementielle le cas échéant
