from abc import abstractmethod
from typing import Tuple
import copy 

from core.pricingengine import PricingEngine, Arguments, Results
from patterns.lazyobject import LazyObject
from timeRW.date import Date

class Instrument(LazyObject):
    
    def __init__(self) -> None:
        super().__init__()
        self._result = None
        self._argument = None
        self._engine = None 

        self._NPV = None
        self._errorEstimate = None
        self._valuationDate = Date()
        self._additionalResults = {}

        self._value = None
        self._isExpired = False

    def setPricingEngine(self, pricingEngine):
        if self._engine:
            self.unregister(self._engine)

        self._engine = pricingEngine
        
        if self._engine:
            self.register(pricingEngine)

        self.update()

    @abstractmethod
    def setupArguments(self, arguments):
        pass
        self._engine._arguments

    def fetchResults(self):
        result = self._engine._results
        self._NPV = result._value
        self._errorEstimate = result._errorEstimate
        self._valuationDate = result._valudationDate
        self._additionalResults = copy.deepcopy(result._additionalResults)

    def result(self, tagname):
        try:
            value = self._additionalResults[tagname]
        except:
            raise Exception("Tag does not exist in the result")
        return value

    def additionalResults(self):
        return self._additionalResults
    
    def calculate(self):
        if not self._calculated:
            if (self._isExpired()):
                self.setupExpired()
                self._calculated = True
            else:
                super().calculate()
    
    def performCalculations(self):
        if self._engine is None:
            raise Exception("Missing Pricing Engine")
        
        self._engine.reset()
        self.setupArguments()
        self._engine.validate()
        self._engine.calculate()
        self.fetchResults()

    def setupExpired(self):
        self._NPV = 0
        self._errorEstimate = 0
        self.valuationDate = Date()
        self.additionalResults = {}

    def isExpired(self):
        pass

    def NPV(self):
        self.calculate()
        if self._NPV is None:
            raise Exception("NPV does not exist")
        return self._NPV

    def errorEstimate(self):
        self.calculate()
        if self._errorEstimate is None:
            raise Exception("error estimate does not exist")
        return self._NPV

    def valuationDate(self):
        self.calculate()
        return self._valuationDate


class InstrumentResults(Results):
    
    def __init__(self):
        super().__init__()
        self._value = None 
        self._errorEstimate = None 
        self._valuationDate = None 
        self._additionalResults = {}

    def reset(self):
        self._value = None 
        self._errorEstimate = None 
        self._valuationDate = None 
        self._additionalResults = {}