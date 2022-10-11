# 1.1 - Introduction

* Async is becoming more & more important in Python
* We want to discover the specificities of the Python model

## 1.2 - Dive into Python asynchronous model

* The goal is to answer the following questions:
    * What is hidden bheind the `async` & `await` keywords?
    * What do they have to do with `asyncio` lib?
    * What `asyncio` is made of and how to rewrite it?
* `asyncio` is the async engine of the standard library


# 2.1 - A world of coroutines

## 2.2 - Coroutines (definition)

* Define a coroutine with `async def` (Python 3.5)

------------

* The coroutine is the return value of the function (like with generator-functions)
* Then it can get arguments like other functions, used by the coroutine object

## 2.3 - Coroutines (execution)

* Body is executed with `await` from an async environment
    * `jupyter-notebook` *REPL* is an async env
* A coroutine is also an async env (so `await` could be used in a coroutine to wait for another one)

------------

* Otherwise you should run it in an event loop or use `asyncio.run` (`asyncio` is in charge or starting the coroutine and waiting for it to stop)

------------

* The event loop is specific to the async engine (`asyncion`), it schedules and executes tasks in a concurrent way (not parallel)

## 2.4 - Coroutines - introspection (`coroutine`)

* The coroutine is the object returned by the function
* The coroutine object has an `__await__` method, meaning that it could be used with an `await`

## 2.5 - Coroutines - introspection (`coroutine_wrapper`)

* This `__await__` method returns an iterator (see methods `__iter__` & `__next__` of the returned object)
* Because coroutines are just a wrapper around Python iteration mechanism: execute step by step a task and interrupt for dealing events

## 2.6 - Coroutines - iteration (`for`)

* So we could write a `for` block to iterate through the body of a coroutine

## 2.7 - Coroutines - iteration (`complex_work` + `for`)

* Our coroutine here does no async work, a more relevant example would use `await`
* The behaviour is the same and we see that our whole coroutine is executed

## 2.8 - Coroutines - iteration (`__await__` + `next`)

* We would see that clearier if the execution was step by step
* What we could do with manual calls to `next` function to get next value of an iterator
* Each interruption is then visible

------------

* The interruption let the loop takes control back, handle incoming events and schedule tasks (suspend or resume)
* It's equivalent to `yield` keyword from generators, `await` is equivalent to `yield from`
    * (`await asyncio.sleep(0)` is a special case for `sleep` that only does a `yield`, the behaviour would be different with a not-null duration)


# 3.1 - Wait for me!

## 3.2 - Awaitables (definition)

* We saw that coroutines are just a special case of async tasks
* Async tasks are objects caracterized by an `__await__` method (we call them *awaitables*)
* This method should return an iterator (not only an iterable!)
* The easiest is to use a generator-function (with `yield`)
* That's how it was done before Python 3.5: a decorator was wrapping a generator to a coroutine

------------

* `ComplexWork` class is equivalent to `complex_work` previous function
* We could use it with `await`!

## 3.3 - Awaitables - iteration

* In the same way, we can now manually iterate over it

## 3.4 - Awaitables (class definition)

* In fact it's not really useful to have a hand-made async task instead of a couritine
* But it let us store a state with this task, and maybe alterate this state from outside of the task to interact with it
* For example the `Waiter` task make us wait that its state becomes `true` (via an external event)
* The code is pretty simple, the task interrupts and loops untils the state is not true

## 3.5 - Awaitables - sychronisation (example)

* We could use this task to synchronize two coroutines:
    * The first one waits the *waiter* object and the second one executes its job and notifies the *waiter*
* We can change sleeping time to check that it's not random and that the first task is correctly waiting
* `gather` is a tools from `asyncio` that let you execute multiple tasks in "parallel"
* Some other uses for `Waiter` could be to handle mutexes for example


# 4.1 - Goldilocks and the three tasks

* French joke because "Goldilocks" is "golden loop"

## 4.2 - Event loops (`run_task`)

* The loop schedules and execute tasks, handle events
* We start by iterating over the task until the final exception

## 4.3 - Event loops (`run_tasks`)

* The previous function handle only one task and schedule nothing
* We improve then the function to take a list of tasks
* *Round-robin* algorithm iterates over all the tasks with a queue
    * We take the first available task and we add it again to the end if it's not finished

## 4.4 - Event loops - execution

* Then we can replace `gather` in our previous examples by this new runner function
* And get the same result than with `asyncio`, even with more complex objects

## 4.5 - Asynchronous environment (`interrupt` + `sleep`)

* Simple interruption is often necessary
* Then we can create an `interact` class that will be equivalent to `yield` or `await sleep(0)`
* Then we have this new task to wait when we want to do an interruption from a coroutine

--------------------

* So we use it to make a `sleep` coroutine that waits for a given duration

## 4.6 - Asynchronous environment - example

* And it works with our `run_tasks` function!
* We see mixed messages from the both coroutines
* The loop doesn't wait for a task to be finished to schedule the next one, it simply waits for an interruption

## 4.7 - Event loops - interactions (`Loop` + `add_task`)

* Our "loop" does not handle interactions yet
* We cannot add new tasks on the fly once the loop is run
* So we replace the function by a class to add a state (the list of tasks)
* `add_task` method to add a new task to the list (and make it an iterator)

## 4.8 - Event loops - interactions (`Loop.run_task`)

* Utility method `run_task` to keep the previous usecase: add a new task and run the loop

## 4.9 - Event loops - interactions (`Loop.current`)

* To interact with the loop from our tasks, they need to have access to the current loop
* Add a class attribute `Loop.current` initialized at the beginning of the loop
    * (in a real environment we would need to renitialize it at each iteration to let have several simultaneous loops)
    * Be careful, this part is not thread-safe, it's just an example

## 4.10 - Event loops - utility functions (`Waiter`)

* `gather` function from `asyncio` would be useful with `run_task`
* We could rewrite it from our `Waiter` task that we have to improve a bit
* We should wait for `n` notifications instead of only one, the task will finish when it will have been notified `n` times

## 4.11 - Event loops - utility functions (`gather`)

* From previous utils, we can then implement `gather`:
    * We create a `Waiter` object that will be used by `gather` and the tasks
    * We wrap every task in coroutines to notify the *waiter* when the task is finished
    * We add all new tasks to the current event loop
    * We wait for the *waiter*, that will finish when all tasks will finish
* We can see simultaneous execution of tasks, sleep times can be updated to see the changes

## 4.12 - Event loops - network utils (_sockets_)

* We want to add a more useful feature to our async engine: sockets!
* The `select` function would be useful, it let us know when a file/socket is ready
* Then we can interrupt the coroutine while the socket is not ready to read/write for the current operation
* Then event loop take control back and can schedule other tasks

## 4.13 - Event loops - network utils (`AIOSocket`)

* On commence par créer la structure de notre classe : une _socket_ et des sélecteurs (lecture & écriture)
* Respect de l'interface des *sockets* (`close`, `fileno`), *context-manager*

* We start with the structure of a new class: a socket with selectors (read é write)
* We respect socket interface (`close` & `fileno`) and context-manager interface

## 4.14 - Event loops - network utils (`AIOSocket.bind`, `listen`, `connect`)

* operations on server/client to allow connection

## 4.15 - Event loops - network utils (`AIOSocket.accept`, `recv`, `send`)

* Read/write operations on the same pattern
* `accept` method returns a socket object of the same type

## 4.16 - Event loops - network utils (`aiosocket`)

* New helper to create an async socket

## 4.17 - Event loops - network utils (exemple)

* We create a server and a client that communicate together, in the same event loop
* The server returns messages reversed
* We can see that nothing blocks, both coroutines are executed/scheduled

# 5.1 - No Future

## 5.2 - Futures

* Our async engine is really inefficient, especially the `sleep` function
* A task should not need to be rescheduled if it waits for a condition that we know is not true yet
* There should be a better way for the loop to know that and only schedules useful tasks

## 5.3 - Futures - asyncio (example)

* In `asyncio` they use a future mechanism for that, that we could easily see
* A future let us wait for a result that has not been computed yet

--------------------

* This goes through `yield` keyword from our async tasks which not always returns `None`, like with `asyncio.sleep` function

## 5.4 - Futures - example (`Future` class)

* Here is a very simple example of a future in the same pattern as our `Waiter` class
* No loop needed in the `__await__` method: it should not be scheduled more than twice
    * One first time to start waiting and a second one after the condition is met to resume the calling task
* When a task executes an `await`, the `yield` value goes through the calling stack and is returned back to the event loop

* The `self` here will let us access to the future from the loop, even if the coroutine only does a `await Future()`
* There is no other way for the loop to access this future object, since it would only have access to the wrapping async task

## 5.5 - Futures - example (`Future.set` + _callback_)

* We can add a `set` method to our future to notify that it's finished
* The method will be in charge of putting that task back in the tasks list of the event loop (to be scheduled by the loop during the next iteration)
* For that we use `self.task` that doesn't exist yet but that will be added to the loop later

## 5.6 - Futures - event loop (`yield` return)

* On the loop side, we have to handle futures
* If the value yielded/returned by the generator is a future, we set its `task` attribute as needed
* And we only reschedule a task if it doesn't return a future (not to schedule it twice: the task will be added when the future will be notified)

* Or futures are currently useless, we have to manually call `set` to trigger them
* We should link them to events, make it automatic

## 5.7 - Futures - time events (`TimeEvent`)

* Simplest events to implement are time events
* The loop knows current time and can trigger actions from that fact
* The goal is to link a time with a future, and use it in the loop

* Then we create a `TimeEvent` class to link the two items
* We need this class to be orderable, so that we can find the next events to trigger

## 5.8 - Futures - time events (`call_later`)

* We add a new `call_later` method to the event loop
* The method takes a time and a future, link then in a `TimeEvent` object and push it in the events queue
* We use an `heapq` to keep this set ordered: the first event will always be the next to execute

## 5.9 - Futures - time events (`Loop.run`)

* In the loop we just have to look at these events at the beginning of the iteration and trigger the next one if needed
* Triggering = notify the future linked to the event
* The effect is immediate, the future add the task to the loop when triggered, and the task will be scheduled in the current iteration of the loop
* The rest of the `run` method stays unchanged

## 5.10 - Futures - utils (`sleep`)

* Then we can rewrite `sleep` function with a future and a time-event
* The coroutine creates a future and add it to the loop with `call_later` method
* And that's all!

* We just need that a coroutine calls `await sleep(...)` to make everything work:
    * The future is instanciated, a time event is linked with it in the loop
    * The task is removed from the tasks list of the loop
    * The loop continues iterating over other tasks and until it mets the time event
    * Then it triggers the notification, the task is re-added to the list
    * The loop schedules the task again

* Indeed it's more advanced in `asyncio`


# 6.1 - For a Few Tools More

## 6.2 - Other tools

* Last versions of Python introduced other tools for async programming
* For example we have async loops (`async for` - not event loops) et async context-managers (`async with`)
* Built on the same pattern than `def` becoming `async def` for coroutines
* They are similar to their sync-equivalents but use special methods that call coroutines

## 6.3 - Async iterables & generators (`__aiter__` + `__anext__`)

* Reminder:
    * Iterable = `__iter__` method that returns an iterator
    * Iterator = `__next__` method that returns the next element at each call, consuming the iterator

* `__aiter__` and `__anext__` are similar to `__iter__` and `__next__`
* `__aiter__` returns an async iterator
* `__aiter__` is a synchronous method

--------------------

* `__anext__` is a coroutine, it returns the next element (and it can use all async tools)

--------------------

* `StopAsyncIteration` is equivalent to `StopIteration`
* `for` loop will be suspended while we wait for the iterator (and the event loop tkaes control back)

## 6.4 - Async iterables (`Arange`)

* `ARange` produce numbers like `range` does, but use an external event to synchronize itself (a `sleep` event)
* Different classes for the iterable and the iterator (`ARange` itself does no async work, it's `ARangeIterator` that does)
* Works perfectly with our async env and our event loop (here we use our `sleep` function and not `asyncio.sleep`)

## 6.5 - Async iterables (`async for`)

* We create a coroutine to be able to use `async for` syntax
* We run the coroutine in our event loop
* (this example is not compatible with *REPL* `await` because it doesn't use `asyncio` tools)

## 6.6 - Async generators (`arange`)

* Async generators make this easier (since Python 3.6)
* `async def` + `yield` created an async gen function
* Async comprehensions (list/gen/dict/set) have also been introduced in Python 3.6 (`[... async for ...]`)

## 6.7 - Async context managers (`__aenter__` + `__aexit__`)

* Reminder:
    * Opening method `__enter__` to setup and return the context
    * Closing method `__exit__` to cleanup, close and handle exceptions

* Asynchronous equivalent to context-managers where `__aenter__` and `__aexit__` methods are coroutines
* Example of a server wrapping one of our sockets to handle basic operations in a context

## 6.8 - Async context managers (`async with`)

* Like before we define a coroutine to use this syntax
* We take the same server as before that returns reversed messages

## 6.9 - Async context managers (`contextlib`)

* `contextlib.asynccontextmanager` has been added in Python 3.7
* Like `contextmanager` that wraps a generator into a context-manager
* Here the decorator wraps the async-generator into an async-context-manager
* `yield` instruction to split the init and the finalization, that returns the context

# 7.1 - Conlusion

## 7.2 - Conclusion

* Everything here is wobbly, this is simply to illustrate the async engine
* Do not replace `asyncio` by this shit, but it's useful to understand how it works internally
* `trio` is also a good lib that implement itts own async engine, and there are other libs like that

## 7.3 - Questions ?
