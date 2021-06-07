"""
simple quotes:
most simple quotes
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.quotes import Quote


class SimpleQuotes(Quote):
    def __init__(self, x) -> None:
        super().__init__()
        self._value = None
        self._setValue(x)

    def value(self):
        return self._value
    
    def _setValue(self,x):
        if self.isValid(x):
            self._value = float(x)
        else:
            self._value = None
    
    def setValue(self,x):
        self._setValue(x)
        if self._value:
            self.notify()
            #self.notify_(x)

    def isValid(self,x):
        try:
            float(x)
        except:
            return False
        return True

    def reset(self):
        self._value = None


if __name__ == "__main__":

    from  patterns.observable import Observer
    class printObserver(Observer):
        def update(self,x = "Null Value Passed"):
            print(x)

    pt1 = printObserver()
    quote1 = SimpleQuotes(2)
    quote1.register(pt1)
    quote1.setValue("3")
