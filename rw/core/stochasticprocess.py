import sys
sys.path.append(".")

from abc import abstractmethod, ABC

from patterns.observable import Observable, Observer
from maths.matrix import Matrix
from maths.array import Array
from timeRW.date import Date
from core.error import RW_Fail, RW_Ensure

"""
multi-dimensional stochastic process class.
This class describes a stochastic process governed by:
d\mathrm{x}_t = \mu(t, x_t)\mathrm{d}t
                      + \sigma(t, \mathrm{x}_t) \cdot d\mathrm{W}_t.
"""

class StochasticProcess(Observer, Observable):

    def __init__(self, discretization_):
        self._discretization = discretization_
    
    @abstractmethod
    def size(self):
        pass

    def factors(self):
        return self.size()

    @abstractmethod
    def initialValues(self):
        pass

    @abstractmethod
    def drift(self,t,x):
        pass

    @abstractmethod
    def diffusion(self,t,x):
        pass

    def expectation(self,t0,x0,dt):
        return self.apply(
            x0,
            self._discretization.covariance(self,t0,x0,dt)
        )
    
    def stdDeviation(self,t0,x0,dt):
        return self._discretization.diffusion(self,t0,x0,dt)

    def covariance(self,t0,x0,dt):
        return self._discretization.covariance(self,t0,x0,dt)
    
    @staticmethod
    def evolve(t0,x0,dt,dw):
        return StochasticProcess.apply(
            StochasticProcess.expectation(t0,x0,dt),
            StochasticProcess.stdDeviation(t0,x0,dt)*dw
        )

    @staticmethod
    def apply(x0,dx):
        return x0 + dx

    def time(self):
        RW_Fail("date/time conversion not supported")

    def update(self):
        self.notify()

    class discretization(ABC):
        
        @staticmethod
        def drift(stochasticProcess_, t0, x0, dt):
            pass

        @staticmethod
        def diffusion(stochasticProcess_, t0, x0, dt):
            pass

        @staticmethod
        def covariance(stochasticProcess_, t0, x0, dt):
            pass


class StochasticProcess1D(StochasticProcess):

    def __init__(self, discretization_):
        super().__init__(discretization_)

    def x0(self):
        raise NotImplementedError

    def size(self):
        return 1

    def initialValues(self):
        return Array(1,self.x0())

    #drift
    def drift(self, t, x):
        if isinstance(x, Array):
            return self._driftArray(t,x)
        if type(x) == int or type(x) == float:
            return self._driftNumeric(t,x)
        RW_Fail("Drift input type not implemented")

    def _driftArray(self,t,x):
        return Array(1,self.drift(t,x[0]))

    @abstractmethod
    def _driftNumeric(self,t,x):
        raise NotImplementedError

    #diffusion
    def diffusion(self, t, x):
        if isinstance(x, Array):
            return self._diffusionArray(t,x)
        if type(x) == int or type(x) == float:
            return self._diffusionNumeric(t,x)
        RW_Fail("Diffusion input type not implemented")

    def _diffusionArray(self,t,x):
        return Matrix(1,1,self.diffusion(t,x[0]))

    @abstractmethod
    def _diffusionNumeric(self,t,x):
        raise NotImplementedError


    def expectation(self, t0, x0, dt):
        if isinstance(x0, Array):
            return self._expectationArray(t0, x0, dt)
        if type(x0) == int or type(x0) == float:
            return self._expectationNumeric(t0, x0, dt)
        RW_Fail("Expectation input type not implemented")

    def _expectationArray(self,t0, x0, dt):
        return Array(1,self.expectation(t0, x0[0], dt))

    def _expectationNumeric(self,t0, x0, dt):
        return self.apply(
            x0,
            self._discretization.drift(self,t0, x0, dt)
        )

    def stdDeviation(self, t0, x0, dt):
        if isinstance(x0, Array):
            return self._stdDeviationArray(t0, x0, dt)
        if type(x0) == int or type(x0) == float:
            return self._stdDeviationNumeric(t0, x0, dt)
        RW_Fail("stdDeviation input type not implemented")

    def _stdDeviationArray(self,t0, x0, dt):
        return Matrix(1,1,self.stdDeviation(t0, x0[0], dt))

    def _stdDeviationNumeric(self,t0, x0, dt):
        return self._discretization.diffusion(self, t0, x0, dt)

    def covariance(self,t0,x0,dt):
        return Matrix(1,1,self.variance(t0, x0[0], dt))

    def variance(self,t0,x0,dt):
        return self._discretization.variance(t0,x0,dt)

    def evolve(self, t0, x0, dt, dw):
        if isinstance(x0, Array) and isinstance(dw, Array):
            return self._evolveArray(t0, x0, dt, dw)
        elif (type(x0) == int or type(x0) == float) and (type(dw) == int or type(dw) == float):
            return self._evolveNumeric(t0, x0, dt, dw)
        RW_Fail("evolve one or more inputs type not implemented")

    def _evolveArray(self, t0, x0, dt, dw):
        return Array(1,self.evolve(t0, x0[0], dt, dw[0]))

    def _evolveNumeric(self, t0, x0, dt, dw):
        return self.apply(self.expectation(t0, x0, dt), self.stdDeviation(t0,x0,dt)*dw)

    def apply(self, x0, dx):
        if isinstance(x0, Array) and isinstance(dx, Array):
            return self._applyArray(x0,dx)
        elif (type(x0) == int or type(x0) == float) and (type(dx) == int or type(dx) == float):
            return self._applyNumeric(x0,dx)
        RW_Fail("apply one or more inputs type not implemented")

    def _applyArray(self,x0,dx):
        return Array(1, self.apply(x0[0],dx[0]))
    
    def _applyNumeric(self,x0,dx):
        return x0 + dx

    class discretization(ABC):
        
        @staticmethod
        def drift(stochasticProcess_, t0, x0, dt):
            pass

        @staticmethod
        def diffusion(stochasticProcess_, t0, x0, dt):
            pass

        @staticmethod
        def variance(stochasticProcess_, t0, x0, dt):
            pass