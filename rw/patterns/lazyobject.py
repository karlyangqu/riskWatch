import sys, os 
sys.path.append(".")

from abc import abstractmethod
from patterns.observable import Observable, Observer

class LazyObject(Observable, Observer):

    def __init__(self) -> None:
        super().__init__()
        self._calculated = False
        self._frozen = False
        self._alwaysForward = False

    def unfreeze(self):
        if (self._frozen):
            self._frozen = False
            self.notify()

    def recalculate(self):
        wasFrozen = self._frozen
        self._calculated = False
        self._frozen = False
        try:
            self.calculate()
        except:
            raise
        finally:
            self._frozen = wasFrozen
            self.notify()

    def freeze(self):
        self._frozen = True

    def alwaysForwardNotifications(self):
        self._alwaysForward = True

    def update(self):
        if (self._calculated) or (self._alwaysForward):
            self._calculated = False
            if not self._frozen:
                self.notify()

    def calculate(self):
        if (not self._calculated) and (not self._frozen):
            self._calculated = True

            try:
                self.performCalculated()
            except:
                self._calculated = False
                raise
                
    @abstractmethod
    def performCalculated(self):
        pass


if __name__ == "__main__":
    import sys,os 
    sys.path.append("../../")
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

    class test(LazyObject):
        def performCalculated(self):
            print("Performing Calc")

    test1 = test()
    test1.calculate()