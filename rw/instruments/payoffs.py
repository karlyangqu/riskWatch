from os import POSIX_FADV_SEQUENTIAL
import sys 
sys.path.append(".")

from core.payoff import Payoff
from core.option import Option, OptionType
from core.error import RW_Fail

class NullPayoff(Payoff):
    
    def name(self):
        return "Null"

    def description(self):
        return self.name()

    def operator(self):
        RW_Fail("dummy payoff given")

class TypePayoff(Payoff):

    def __init__(self, type_) -> None:
        self._type =  OptionType[type_.capitalize()]

    def optionType(self):
        return self._type

    def description(self):
        return self.name() + " " + str(self.optionType())

class FloatingTypePayoff(TypePayoff):
    
    def name(self):
        return "FloatingType"
    
    def operator(self, price, strike):
        if self._type is OptionType.Call:
            return max( price - strike , 0.0)
        elif self._type is OptionType.Put:
            return max( strike - price, 0.0)
        else:
            RW_Fail("unknown/illegal option type")

class StrikedTypePayoff(TypePayoff):

    def __init__(self,type_,strike_):
        super().__init__(type_)
        self._strike = strike_

    def description(self):
        return super().description() + ", " + str(self.strike) + " strike"

    def strike(self):
        return self._strike
        
class PlainVanillaPayoff(StrikedTypePayoff):
    
    def __init__(self, type_, strike_):
        super().__init__(type_, strike_)

    def name(self):
        return "Vanilla"

    def operator(self, price):
        if self._type is OptionType.Call:
            return max( price - self._strike , 0.0)
        elif self._type is OptionType.Put:
            return max( self._strike - price, 0.0)
        else:
            RW_Fail("unknown/illegal option type")
    
class PercentageStrikePayoff(StrikedTypePayoff):

    def __init__(self, type_, moneyness_):
        super().__init__(type_, moneyness_)

    def name(self):
        return "PercentageStrike"

    def operator(self, price):
        if self._type is OptionType.Call:
            return price * max( 1.0 - self._strike , 0.0)
        elif self._type is OptionType.Put:
            return price * max( self._strike - 1.0, 0.0)
        else:
            RW_Fail("unknown/illegal option type")
    
class AssetOrNothingPayoff(StrikedTypePayoff):

    def __init__(self, type_, strike_):
        super().__init__(type_, strike_)

    def name(self):
        return "AssetOrNothing"

    def operator(self, price):
        if self._type is OptionType.Call:
            if price > self._strike:
                return price
            else:
                return 0.0

        elif self._type is OptionType.Put:
            if self._strike > price:
                return price 
            else:
                return 0.0

        RW_Fail("unknown/illegal option type")           

class CashOrNothingPayoff(StrikedTypePayoff):

    def __init__(self, type_, strike_, cashPayoff_):
        super().__init__(type_, strike_)    
        self._cashPayoff = cashPayoff_
        
    def name(self):
        return "CashOrNothing"

    def description(self):
        return super().description() + ", " + str(self._cashPayoff) + " cash payoff"

    def operator(self, price):
        if self._type is OptionType.Call:
            if price > self._strike:
                return self._cashPayoff
            else:
                return 0.0

        elif self._type is OptionType.Put:
            if self._strike > price:
                return self._cashPayoff
            else:
                return 0.0

        RW_Fail("unknown/illegal option type")     

class GapPayOff(StrikedTypePayoff):

    def __init__(self, type_, strike_, secondStrike_):
        super().__init__(type_, strike_)
        self._secondStrike = secondStrike_

    def name(self):
        return "Gap"

    def description(self):
        return super().description() + ", " + self.secondStrike() + " strike payoff"

    def secondStrike(self):
        return self._secondStrike

    def operator(self, price):
        if self._type is OptionType.Call:
            if price > self._strike:
                return price - self._secondStrike
            else:
                return 0.0

        elif self._type is OptionType.Put:
            if self._strike > price:
                return self._secondStrike - price
            else:
                return 0.0

#furthur development
class SuperFundPayoff:
    pass

class SuperSharePayoff:
    pass