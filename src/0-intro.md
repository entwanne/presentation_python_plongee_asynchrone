# Dive into Python asynchronous model
### Without drowning!

<center><img src="logo_pres.png" style="height: 15em;" /></center>
<div align="right"><img src="cc_by_sa.svg" style="width: 5em;" /></div>

```python skip
%load_ext reopenable
import asyncio

class Loop(metaclass=Reopenable): pass
class AIOSocket(metaclass=Reopenable): pass
```

## Dive into Python asynchronous model

* `asyncio` is not the only async engine
* `async` and `await` could be used outside of `asyncio`
* How could `asyncio` be rewritten?
