import sys 
sys.path.append(".")

from enum import Enum
from core.instrument import Instrument
from core.pricingengine import Arguments, Results
from core.error import RW_Require

class OptionType(Enum):
    Put = -1
    Call = 1

    def __str__(self):
        return self.name

class Option(Instrument):
    def __init__(self, payoff, execrise) -> None:
        super().__init__()
        self._payoff = payoff
        self._execrise = execrise

    @property
    def type(self):
        return self._type
 
    @type.setter
    def type(self,type_):
        self._type = OptionType[type_.capitalize()]

    @property
    def payoff(self):
        return self._payoff
    
    @property
    def exercise(self):
        return self._execrise
        
    def setupArguments(self):
        self._arguments = self.Argument(self._payoff, self._execrise)

    class Arguments(Arguments):
        def __init__(self, payoff = None, execrise = None):
            super().__init__()
            self._payoff = payoff
            self._execrise = execrise

        def validate(self):
            RW_Require(self, "_payoff")
            RW_Require(self, "_execrise")


# addtional Optional Results
class Greeks(Results):
    def __init__(self):
        super().__init__()
        self._delta = None
        self._gamma = None
        self._theta = None 
        self._vega = None 
        self._rho = None
        self.dividendRho = None
    
    def reset(self):
        self._delta = None
        self._gamma = None
        self._theta = None 
        self._vega = None 
        self._rho = None
        self.dividendRho = None

# additional Otion Result 
class MoreGreeks(Results):
    def __init__(self):
        super().__init__()
        self._itmCashProbability = None 
        self._deltaForward = None
        self._elasticity = None
        self._thetaPerDay = None
        self._strikeSensitivity = None
    
    def reset(self):
        self._itmCashProbability = None 
        self._deltaForward = None
        self._elasticity = None
        self._thetaPerDay = None
        self._strikeSensitivity = None        


if __name__ == "__main__":
    Option.Arguments()
    print("succeed")