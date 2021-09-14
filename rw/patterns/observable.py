import weakref
from abc import ABC,abstractmethod

class Observable:

    def __init__(self) -> None:
        self._observers = weakref.WeakSet()

    def register(self, o):
        self._observers.add(o)

    def unregister(self, o):
        self._observers.remove(o)

    def unregisterAll(self):
        self._observers = weakref.WeakKeyDictionary()

    def notify(self):
        for o in self._observers:
            o.update()

    def notify_(self, x):
        for o in self._observers:
            o.update(x)

class Observer(ABC):
    @abstractmethod
    def update(self):
        pass