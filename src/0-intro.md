# Plongée au cœur du modèle asynchrone Python 
### Sans boire la tasse !
#### <div align="right">Antoine "entwanne" Rozo</div>

<div align="right"><img src="schtroumpf_flat_rounded.png" style="width: 5em;" /></div>

<div align="right"><small><i>CC BY-SA</i></small></div>

```python skip
%load_ext reopenable
import asyncio

class Loop(metaclass=Reopenable): pass
class AIOSocket(metaclass=Reopenable): pass
```

--------------------

<center><img src="logos.png" style="height: 20em;" /></center>

## Plongée au cœur du modèle asynchrone Python 

* `asyncio` n'est pas le seul moteur asynchrone
* `async` et `await` ne lui sont pas intrinsèquement liés
* Comment réécrire `asyncio` ?

* <https://github.com/entwanne/presentation_python_plongee_asynchrone>
