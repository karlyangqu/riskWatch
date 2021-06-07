
from patterns.observable import Observable, Observer
from abc import ABC, abstractmethod

class PricingEngine(Observable, Observer):

    def __init__(self, argument = None, result = None) -> None:
        super().__init__()
        self._arguments = argument
        self._results = result

    def getArguments(self):
        return self._arguments

    def getResults(self):
        return self._results

    def reset(self):
        self._arguments.reset()

    def update(self):
        self.notify()

    @abstractmethod
    def calculate(self):
        pass
    

class Arguments(ABC):
    def __init__(self):
        pass 
    
    @abstractmethod
    def validate(self):
        pass


class Results(ABC):
    def __init__(self):
        pass 

    @abstractmethod
    def reset(self):
        pass 

    
