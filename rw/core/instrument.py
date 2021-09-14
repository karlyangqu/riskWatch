from abc import abstractmethod
from typing import Tuple
import copy 

from core.pricingengine import PricingEngine, Arguments, Results
from core.error import RW_Ensure
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

    def NPV(self):
        self.calculate()
        RW_Ensure((self._NPV is not None), "NPV not provided")
        return self._NPV

    def errorEstimate(self):
        self.calculate()
        RW_Ensure((self._errorEstimate is not None), "error estimate not provided")
        return self._NPV

    def valuationDate(self):
        self.calculate()
        return self._valuationDate

    def result(self, tagname):
        try:
            value = self._additionalResults[tagname]
        except:
            raise Exception("Tag does not exist in the result")
        return value

    @property
    def additionalResults(self):
        return self._additionalResults

    def isExpired(self):
        pass

    def setPricingEngine(self, pricingEngine):
        if self._engine:
            self.unregister(self._engine)

        self._engine = pricingEngine
        
        if self._engine:
            self.register(pricingEngine)

        self.update()

    @abstractmethod
    def setupArguments(self,argument_):
        pass
    
    def fetchResults(self, result_):
        
        RW_Ensure((result_ is None),"no results returned from pricing engine")
        self._NPV = result_._value
        self._errorEstimate = result_._errorEstimate
        self._valuationDate = result_._valudationDate
        self._additionalResults = copy.deepcopy(result_._additionalResults)

    def calculate(self):

        if not self._calculated:
            if (self._isExpired()):
                self.setupExpired()
                self._calculated = True
            else:
                super().calculate()

    def setupExpired(self):

        self._NPV = 0
        self._errorEstimate = 0
        self.valuationDate = Date()
        self.additionalResults = {}

    def performCalculations(self):
        
        RW_Ensure((self._engine is not None),"null pricing engine")
        self._engine.reset()
        self.setupArguments(self._engine.getArguments())
        self._engine.getArguments().validate()
        self._engine.calculate()
        self.fetchResults(self._engine.getResults())

    class results(Results):
    
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

        def __call__(self, tag):
            return self._additionalResults[tag]
        
