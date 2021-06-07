"""
Basic payoff:
Abstract base class for option payoffs
"""

from patterns.visitor import Component
from abc import abstractmethod

class Payoff(Component):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def operator(self):
        pass

    # accept method from Componet