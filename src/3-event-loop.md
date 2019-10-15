# Boucles événementielles

## Boucles événementielles

```python
def run_task(task):
    it = task.__await__()

    while True:
        try:
            next(it)
        except StopIteration:
            break
```

--------------------

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

--------------------

```python
run_tasks(simple_print(1), ComplexWork(), simple_print(2), simple_print(3))
```

```python
waiter = Waiter()
run_tasks(wait_job(waiter), count_up_to(waiter, 5))
```

--------------------

```python
class interrupt:
    def __await__(self):
        yield
```

```python
import time

async def sleep_until(t):
    while time.time() < t:
        await interrupt()

async def sleep(duration):
    await sleep_until(time.time() + duration)
```

--------------------

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

--------------------

```python
class Loop:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task.__await__())

    def run(self):
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.tasks.append(task)

    def run_task(self, task):
        self.add_task(task)
        self.run()
```

```python
loop = Loop()
loop.run_task(print_messages('foo', 'bar', 'baz'))
```

--------------------

```python
class Loop:
    current = None

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task.__await__())

    def run(self):
        Loop.current = self
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.tasks.append(task)

    def run_task(self, task):
        self.add_task(task)
        self.run()
```

--------------------

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
loop.run_task(gather(print_messages('foo', 'bar', 'baz'),
    print_messages('aaa', 'bbb', 'ccc', sleep_time=0.7)))
```
