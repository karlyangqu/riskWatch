"""
Basic payoff:
Abstract base class for option payoffs
"""
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patterns.visitor import Component, Visitor
from core.error import RW_Fail, RW_TypeCheck

from abc import abstractmethod

class Payoff(Component):

    #@abstractmethod
    def name(self):
        pass

    #@abstractmethod
    def description(self):
        pass

    #@abstractmethod
    def operator(self):
        pass

    # accept method from Componet
    # type check need to be revisit
    def accept(self,visitor):
        RW_TypeCheck(visitor, Visitor, "not a payoff visitor")
        visitor.visit(self)

if __name__ == "__main__":

    payoff = Payoff()
    print(issubclass(type(payoff),Payoff))
    RW_TypeCheck(payoff,Payoff)
    print("succedd")