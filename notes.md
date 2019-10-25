# 1.1 - Introduction

* Antoine, developpeur Python depuis une dizaine d'années
* L'asynchrone a pris beaucoup d'ampleur dans Python
* Découvrir les subtilités du modèle asynchrone Python

## 1.2 - Logos

* En télétravail chez PeopleDoc depuis 2018
* Contributeur aux contenus sur ZdS
* Appris l'asynchrone sur ZesteDeSavoir, expérimenté chez PeopleDoc

## 1.3 - Plongée au cœur du modèle asynchrone Python

* Le but est de répondre aux questions suivantes :
    * Que cachent les mots-clés `async` et `await` ?
    * Quel est leur rapport avec `asyncio` ?
    * De quoi est fait `asyncio` et comment le réécrire ?
* `asyncio` est le moteur asynchrone de la bibliothèque standard


# 2.1 - Un monde de coroutines

## 2.2 - Coroutines (définition)

* Définition d'une coroutine avec `async def` (Python 3.5)
* La coroutine est la valeur de retour de la fonction (comme pour les générateurs)
* Peut donc recevoir des arguments comme toute fonction, utilisés par la coroutine

## 2.3 - Coroutines (exécution)

* Le contenu d'une coroutine est exécuté avec `await` depuis un environnement asynchrone
* C'est le cas du *REPL* `jupyter-notebook`
* Une coroutine est aussi un environnement asynchrone (donc `await` peut y être utilisé pour en attendre une autre)
* Il faut sinon la lancer dans une boucle événementielle ou utiliser `asyncio.run` (`asyncio` se charge de démarrer la coroutine et attendre qu'elle se termine)
* La boucle événementielle est propre au moteur asynchrone (`asyncio`), elle cadence et exécute les tâches de façon concurrente

## 2.4 - Coroutines - introspection (`coroutine`)

* La coroutine est donc le retour de la fonction
* Une coroutine possède une méthode `__await__`, signifiant qu'elle peut être utilisée derrière un `await`

## 2.5 - Coroutines - introspection (`coroutine_wrapper`)

* Cette méthode `__await__` renvoie un itérateur (reconnaissable aux méthodes `__iter__` & `__next__`)
* Parce que la coroutine n'est qu'un enrobage autour du principe d'itération : exécuter un traitement pas à pas et s'interrompre pour attendre des événements

## 2.6 - Coroutines - itération (`for`)

* On peut donc écrire un bloc `for` pour parcourir le contenu d'une coroutine

## 2.7 - Coroutines - itération (`complex_work` + `for`)

* Notre coroutine ici ne fait rien d'asynchrone, un exemple plus parlant utiliserait des `await`
* Le comportement est le même et on voit bien que toute notre coroutine est exécutée

## 2.8 - Coroutines - itération (`__await__` + `next`)

* On le verrait cependant plus clairement si l'exécution se faisait pas à pas
* Ce que l'on peut obtenir en faisant manuellement les appels à `next`
* Chaque interruption devient alors visible
* L'interruption permet à la boucle de reprendre la main, de gérer les événements et de cadencer les tâches (suspendre ou continuer)
* C'est équivalent au `yield` des générateurs, `await` étant similaire à `yield from`
    * (`await asyncio.sleep(0)` est un cas particulier de `sleep` qui fait juste un `yield`, le comportement serait différent avec un temps non nul)


# 3.1 - Attendez-moi !

## 3.2 - Awaitables (définition)

* On a vu les coroutines, qui ne sont qu'un cas particulier de tâches asynchrones
* Les tâches asynchrones sont les objets caractérisés par une méthode `__await__` (on parle alors d'*awaitables*)
* Cette méthode doit renvoyer un itérateur (pas un itérable !)
* Le plus simple est alors d'utiliser une méthode génératrice (`yield`)
* C'était d'ailleurs la manière de faire avant Python 3.5 : un décorateur transformait un générateur en coroutine

* La classe `ComplexWork` est équivalente à la fonction `complex_work` précédente
* On peut bien sûr l'utiliser avec `await`

## 3.3 - Awaitables - itération

* De la même manière, on peut donc itérer manuellement dessus

## 3.4 - Awaitables (définition classe)

* Il est finalement peu utile d'avoir une tâche asynchrone "maison" plutôt qu'une coroutine
* Mais cela peut servir à stocker un état, pour l'altérer depuis l'extérieur et interagir avec la tâche
* Par exemple la tâche `Waiter` permet d'attendre le temps que son état passe à `True` (via un événement extérieur)
* Le code est relativement simple, la tâche s'interrompt et boucle tant que l'état n'est pas vrai

## 3.5 - Awaitables - sychronisation (exemple)

* On peut l'utiliser pour synchroniser deux coroutines :
    * Une première attend le *waiter* et une seconde exécute son traitement avant de le notifier au *waiter*
* On peut faire varier le temps de `sleep` pour vérifier que ce n'est pas un hasard et que la tâche attend bien
* `gather` est un utilitaire d'`asyncio` pour exécuter plusieurs tâches en "parallèle"
* D'autres utilisations de `Waiter` sont possibles pour gérer par exemple des verrous (*mutex*)


# 4.1 - Boucle d'or et les trois tâches

## 4.2 - Boucles événementielles (`run_task`)

* Cadencer et exécuter les tâches, tenir compte des événements
* On commence par simplement parcourir la tâche jusqu'à l'exception finale

## 4.3 - Boucles événementielles (`run_tasks`)

* La fonction précédente ne gère qu'une tâche et ne cadence rien
* On améliore donc la fonction pour prendre en compte une liste de tâches
* Algorithme de *round-robin* pour itérer sur toutes les tâches, à l'aide d'une queue
    * On prend la première tâche dispo et on rajoute la tâche à la fin si elle continue

## 4.4 - Boucles événementielles - exécution

* Cela nous permet de remplacer `gather` dans nos exemples précédents
* Et d'obtenir le même résultat qu'avec `asyncio`, même avec nos objets complexes

## 4.5 - Environnement asynchrone (`interrupt` + `sleep`)

* L'interruption simple est souvent nécessaire
* On peut donc créer une classe `interrupt` qui sera équivalente au `yield` / `await sleep(0)`
* Ce qui nous permet d'avoir une tâche à attendre pour créer une interruption depuis des coroutines
* On s'en sert donc pour réaliser une coroutine `sleep` attendant un certain nombre de secondes

## 4.6 - Environnement asynchrone - exemple

* Et ça marche avec notre fonction `run_tasks`
* On boit bien les messages des deux coroutines qui s'intermêlent
* La boucle n'attend pas qu'une tâche soit terminée avant de passer à la suivante, juste une interruption

## 4.7 - Boucles événementielles - interactions (`Loop` + `add_task`)

* Notre "boucle" ne permet pas pour le moment les interactions
* On ne peut pas ajouter de nouvelles tâches après le lancement
* On remplace donc la fonction par une classe pour ajouter un état (la liste des tâches)
* Méthode `add_task` ajoutant une tâche à la liste (la transformant en itérateur)

## 4.8 - Boucles événementielles - interactions (`Loop.run_task`)

* Méthode utilitaire `run_task` pour reprendre le cas d'utilisation précédent : ajouter une tâche et lancer la boucle

## 4.9 - Boucles événementielles - interactions (`Loop.current`)

* Pour interagir avec la boucle depuis nos tâches, il leur faut avoir accès à la boucle courante
* Ajout d'un attribut de classe `Loop.current` initialisé au lancement de la boucle
    * (dans un vrai environnement il faudrait la réinitialiser à chaque tour pour permettre à plusieurs boucles de coexister)
    * Attention, le traitement n'est pas *thread-safe*, il ne s'agit que d'un exemple

## 4.10 - Boucles événementielles - utilitaires (`Waiter`)

* L'utilitaire `gather` d'`asyncio` nous serait bien utile avec `run_task`
* On peut le recoder en reprenant notre classe `Waiter` et l'améliorant un peu
* Il suffit d'attendre `n` notifications plutôt qu'une seule, la tâche se terminera après avoir été notifiée `n` fois

## 4.11 - Boucles événementielles - utilitaires (`gather`)

* À l'aide des précédents utilitaires, on peut donc implémenter `gather` :
    * On instancie un `Waiter` qui sera utilisé par `gather` et les tâches
    * On wrappe les tâches dans des coroutines pour notifier le *waiter* après le traitement
    * On ajoute toutes les tâches à la boucle événementielle courante
    * Et on attend le *waiter*, attente qui se terminera donc après l'exécution de toutes les tâches
* On remarque bien l'exécution simultanée, on peut faire varier les temps de pause pour observer les changements

## 4.12 - Boucles événementielles - utilitaires réseau (_sockets_)

* On peut agrémenter notre moteur de fonctionnalités plus utiles : des *sockets*
* La fonction `select` nous sera pour cela utile, elle permet de savoir quand un fichier est prêt
* Il suffit alors d'interromptre la coroutine tant que la _socket_ n'est pas prête en lecture/écriture pour l'opération
* La boucle événementielle reprendra la main et pourra continuer ses traitements

## 4.13 - Boucles événementielles - utilitaires réseau (`AIOSocket`)

* On commence par créer la structure de notre classe : une _socket_ et des sélecteurs (lecture & écriture)
* Respect de l'interface des *sockets* (`close`, `fileno`), *context-manager*

## 4.14 - Boucles événementielles - utilitaires réseau (`AIOSocket.bind`, `listen`, `connect`)

* Opérations de connexion pour clients & serveurs

## 4.15 - Boucles événementielles - utilitaires réseau (`AIOSocket.accept`, `recv`, `send`)

* Opérations de lecture/écriture sur le même modèle
* La méthode `accept` renvoie un objet *socket* du même type

## 4.16 - Boucles événementielles - utilitaires réseau (`aiosocket`)

* *Helper* pour instancier une socket asynchrone

## 4.17 - Boucles événementielles - utilitaires réseau (exemple)

* Création d'un serveur et d'un client qui communiquent ensemble, dans la même boucle événementielle
* Le serveur renvoie le message inversé
* On constate que rien n'est bloquant puisque les deux coroutines ont pu s'exécuter


# 5.1 - No Future

## 5.2 - Futures

* Notre moteur asynchrone est globalement inefficace, notamment la fonction `sleep`
* Une tâche n'est pas censée avoir besoin d'être reprogrammée si elle attend une condition que l'on sait non remplie
* Il faudrait un moyen pour que la boucle soit en connaissance de cela et ne cadence que les tâches utiles

## 5.3 - Futures - asyncio (exemple)

* Il existe pour cela un mécanisme de *futures* dans `asyncio`, que l'on peut facilement mettre en évidence
* Une *future* permet d'attendre un résultat qui n'a pas encore été calculé
* Cela passe par le `yield` de nos tâches asynchrones qui n'est pas obligé de renvoyer `None` à la boucle, comme dans le cas d'`asyncio.sleep`

## 5.4 - Futures - exemple (classe `Future`)

* Voici un exemple très simple de *future* sur le modèle de la classe `Waiter`
* Pas de boucle dans la méthode `__await__`, celle-ci ne devant pas être programmé plus de deux fois :
    * une première fois pour lancer l'attente, une seconde après que la condition soit remplie pour reprendre le travail de la tâche appelante
* Quand une tâche fait un `await`, la valeur du `yield` remonte le flux des appels jusqu'à la boucle

* Le `self` permettra ici d'avoir accès à la *future* depuis la boucle, même si la coroutine a juste fait un `await Future()`
* Il n'y aurait pas d'autre moyen pour la boucle d'avoir accès à cette *future*, puisqu'elle n'a sinon de référence que vers la tâche asynchrone englobante

## 5.5 - Futures - exemple (`Future.set` + _callback_)

* On peut agrémenter notre *future* d'une méthode `set` pour signaler que le traitement est terminé
* La méthode se chargera de renvoyer notre taĉhe dans les tâches à exécuter de la boucle (pour être prise en compte à la prochaine itération)
* Pour cela on utilise `self.task` qui n'existe pas pour l'instant, mais qui sera ajouté par la boucle

## 5.6 - Futures - boucle événementielle (retour `yield`)

* Du côté de la boucle, on peut traiter le cas des *futures*
* Si la valeur renvoyée par le générateur est une *future*, on lui *sette* l'attribut `task` comme convenu
* Et on ne reprogramme la tâche que si elle n'a pas envoyé de *future* (pas de doublon : la tâche sera ajoutée quand la *future* sera notifiée)

* Nos *futures* sont pour l'instant inutiles, nous devons manuellement appeler `set` pour les déclencher
* Il faudrait pouvoir les lier à des événements, rendre le tout automatique

## 5.7 - Futures - événements temporels (`TimeEvent`)

* Les événements les plus simples à mettre en place sont les temporels
* La boucle a conscience de l'heure actuelle et peut déclencher des actions en fonction
* Le but sera d'associer un temps à une *future*, et d'utiliser cela dans la boucle

* On crée donc une classe `TimeEvent` pour associer les deux éléments
* On a besoin que la classe soit ordonnable, pour trouver les prochains événements à déclencher

## 5.8 - Futures - événements temporels (`call_later`)

* On ajoute une méthode `call_later` à la boucle
* La méthode prend un temps et une future, les associe dans un `TimeEvent` et l'ajoute à la queue des événéments
* On utilise une `heapq` pour garder un ensemble ordonné : le premier événement sera toujours le prochain à exécuter

## 5.9 - Futures - événements temporels (`Loop.run`)

* Dans notre boucle, il nous suffit de regarder ces événements en début de boucle et de déclencher le suivant si besoin
* Déclencher = notifier la *future* associée à l'événement
* L'effet sera donc immédiat, la *future* ajoutera la tâche à la boucle, qui sera tout de suite prise en compte
* Le reste de la méthode `run` ne change pas

## 5.10 - Futures - utilitaires (`sleep`)

* On peut alors réécrire `sleep` avec une *future* et un *time-handler*
* La coroutine instancie une *future* et l'ajoute à la boucle via `call_later`
* Et c'est tout

* Il suffit qu'une coroutine appelle `await sleep(...)` pour que tout se mette en place :
    * La *future* est instanciée, un événement temporel lui est associé dans la boucle
    * La tâche est retirée de la liste des tâches à traiter
    * La boucle continue d'itérer, jusqu'à ce que l'événement temporel se produise
    * Elle déclenche alors la notification, la tâche est réajoutée à la liste
    * La boucle reprend l'exécution de la tâche

* C'est bien sûr plus évolué dans `asyncio`


# 6.1 - Et pour quelques outils de plus

## 6.2 - Autres outils

* Python a continué d'évoluer après la 3.5, et d'ajouter d'autres outils pour la programmation asynchrone
* Ont notamment été ontroduits les boucles asynchrones (`async for`) et les gestionnaires de contexte asynchrones (`async with`)
* Conçus sur le même modèle que `def`devenant `async def` pour une coroutine
* Ils sont similaires à leurs équivalents synchrones mais utilisent des méthodes spéciales qui font appel à des coroutines

## 6.3 - Itérables et générateurs asynchrones (`__aiter__` + `__anext__`)

* Rappel :
    * Itérable = `__iter__` qui renvoie un itérateur
    * Itérateur = `__next__` qui renvoie le prochain élément

* `__aiter__` et `__anext__` semblables à `__iter__` et `__next__`
* `__aiter__` renvoie un itérateur asynchrone
* `__aiter__` est une méthode synchrone
* `__anext__` est une coroutine, renvoyant l'élément suivant (et pouvant utiliser tous les outils asynchrones)
* `StopAsyncIteration` équivalent à `StopIteration`
* Le `for` sera suspendu le temps de l'attente de l'itérateur (rendant la main à la boucle événementielle)

## 6.4 - Itérables asynchrones (`Arange`)

* `ARange` produit des nombres comme `range`, mais se synchronise sur un événement extérieur (ici un `sleep`)
* Classes différentes pour l'itérable et son itérateur (`ARange` en elle-même n'a rien d'asynchrone, c'est `ARangeIterator` qui l'est)
* S'accomode parfaitement bien de notre environnement asynchrone et sa boucle (c'est `sleep` qui est utilisé et non `asyncio.sleep`)

## 6.5 - Itérables asynchrones (`async for`)

* Création d'une coroutine pour avoir accès à la syntaxe `async for`
* Lancement dans notre boucle événementielle
* (l'exemple n'est pas compatible avec l'`await` du REPL, puisque n'est pas fait avec `asyncio`)

## 6.6 - Générateurs asynchrones (`arange`)

* Les générateurs asynchrones simplifies la chose (Python 3.6)
* `async def` + `yield` => générateur asynchrone
* Ont aussi été introduites les intensions (listes/générateurs/dict/sets) asynchrones (`[... async for ...]`)

## 6.7 - Gestionnaires de contexte asynchrones (`__aenter__` + `__aexit__`)

* Rappel :
    * Méthode d'ouverture `__enter__` qui renvoie le contexte
    * Méthode de fermeture `__exit__` qui clôt proprement et gère les exceptions

* Équivalent asynchrone où `__aenter__` et `__aexit__` sont des coroutines
* Exemple de serveur *wrappant* une de nos *sockets* pour gérer les opérations de base dans un contexte

## 6.8 - Gestionnaires de contexte asynchrones (`async with`)

* Idem, coroutine pour pouvoir utiliser la syntaxe
* Reprend le principe du précédent serveur qui renvoie le message inversé

## 6.9 - Gestionnaires de contexte asynchrones (`contextlib`)

* Ajout de `contextlib.asynccontextmanager` (Python 3.7)
* Comme `contextmanager` qui permettait de transformer un générateur en *ctx-manager*
* Ici le décorateur transforme un générateur asynchrone en contexte asynchrone
* Instruction `yield` pour la séparation de l'init et de la fermeture, renvoyant le contexte


# 7.1 - Conlusion

## 7.2 - Conclusion

* Tout ce qui est présenté est bancal, il ne s'agit que d'illustrer
* Il n'est pas question de réellement remplacer `asyncio`, juste de comprendre son fonctionnement
* `trio` est aussi une bonne lib qui implémente son propre moteur asynchrone, et il y en a d'autres

## 7.3 - Questions ?
