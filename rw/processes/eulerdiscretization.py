#make sure this works, might be circular references

import sys
sys.path.append(".")

import math

from core.stochasticprocess import StochasticProcess,StochasticProcess1D

class EulerDiscretization(StochasticProcess.discretization, StochasticProcess1D.discretization):
    
    def drift(process_,t0,x0,dt):
        return process_.drift(t0,x0) * dt

    def diffusion(process_,t0,x0,dt):
        return process_.diffusion(t0,x0) * math.sqrt(dt)

    def covariance(process_,t0,x0,dt):
        sigma = process_.diffusion(t0,x0)
        return sigma * sigma.transpose() * dt

    def variance(process_,t0,x0,dt):
        sigma = process_.diffusion(t0, x0)
        return sigma * sigma * dt

if __name__ == "__main__":
    EulerDiscretization()
    print("")