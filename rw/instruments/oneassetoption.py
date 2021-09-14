import sys 
sys.path.append(".")

from core.option import Option
from core.instrument import Instrument
from core.option import Greeks, MoreGreeks
from core.pricingengine import GenericEngine
from core.event import Event, simple_event
from core.error import RW_Require, RW_Ensure, RW_TypeCheck

class OneAssetOption(Option):

    def __init__(self, payoff = None, execrise = None):

        Option.__init__(self,payoff, execrise)
        self._delta = None
        self._deltaForward = None
        self._elasticity = None
        self._gamma = None
        self._theta = None
        self._thetaPerDay = None
        self._vega = None
        self._rho = None
        self._dividendRho = None
        self._strikeSensitivity = None
        self._itmCashProbability = None

    def isExpired(self):
        return simple_event(self._execrise.lastDate()).hasOccurred()

    def delta(self):
        self.calculate()
        RW_Require("_delta")
        return self._delta

    def deltaForward(self):
        self.calculate()
        RW_Require("_deltaForward")
        return self._deltaForward

    def elasticity(self):
        self.calculate()
        RW_Require("_elasticity")
        return self._elasticity

    def gamma(self):
        self.calculate()
        RW_Require("_gamma")
        return self._gamma

    def theta(self):
        self.calculate()
        RW_Require("_theta")
        return self._theta

    def thetaPerDay(self):
        self.calculate()
        RW_Require("_thetaPerDay")
        return self._thetaPerDay

    def vega(self):
        self.calculate()
        RW_Require("_vega")
        return self._vega

    def rho(self):
        self.calculate()
        RW_Require("_rho")
        return self._rho

    def dividendRho(self):
        self.calculate()
        RW_Require("_dividendRho")
        return self._dividendRho

    def strikeSensitivity(self):
        self.calculate()
        RW_Require("_strikeSensitivity")
        return self._strikeSensitivity

    def itmCashProbability(self):
        self.calculate()
        RW_Require("_itmCashProbability")
        return self._itmCashProbability

    def setupExpired(self):
        Option.setupExpired(self)
        self._delta = None
        self._deltaForward = None
        self._elasticity = None
        self._gamma = None
        self._theta = None
        self._thetaPerDay = None
        self._vega = None
        self._rho = None
        self._dividendRho = None
        self._strikeSensitivity = None
        self._itmCashProbability = None

    def fetchResults(self,result_):
        RW_TypeCheck(type(result_), Greeks,"no greeks returned from pricing engine")
        self._delta = result_._delta
        self._gamma = result_._gamma
        self._theta = result_._theta
        self._vega = result_._vega
        self._rho = result_._rho
        self._dividendRho = result_._dividendRho
        
        RW_TypeCheck(type(result_), MoreGreeks,"no greeks returned from pricing engine")
        self._deltaForward = result_._deltaForward
        self._elasticity = result_._elasticity
        self._thetaPerDay = result_._thetaPerDay
        self._strikeSensitivity = result_._strikeSensitivity
        self._itmCashProbability = result_._itmCashProbability

    class results(Instrument.results, Greeks, MoreGreeks):
        def reset(self):
            self._delta = 1
            Instrument.results.reset(self)
            Greeks.reset(self)
            MoreGreeks.reset(self)

    class engine(GenericEngine):
        pass


if __name__ == "__main__":
    result = OneAssetOption.results()
    result.reset()
    print(result._delta)
    print("succeeded")