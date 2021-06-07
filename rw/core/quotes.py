"""
Basic quotes:
Brief purely virtual base class for market observables
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from abc import ABC,abstractmethod
from patterns.observable import Observable

class Quote(Observable): 
    
    @abstractmethod
    def value():
        pass 

    @abstractmethod
    def isValid():
        pass

