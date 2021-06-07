import weakref
from abc import ABC,abstractmethod

class Observable:

    def __init__(self) -> None:
        self._observers = weakref.WeakKeyDictionary()

    def register(self, o):
        self._observers[o] = 1

    def unregister(self, o):
        del self._observers[o]

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