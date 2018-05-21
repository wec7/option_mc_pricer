import math

import numpy as np


class EuropeanVanillaPricing(object):
    def __init__(self, param):
        self.method = param.method
        self.pc = param.pc
        self.S = param.S
        self.K = param.K
        self.T = param.T
        self.r = param.r
        self.sigma = param.sigma
        if self.method == 'mc':
            self.iterations = param.iterations

    def get_price(self):
        if self.method == 'mc':
            return self.get_mc_price()
        elif self.method == 'exact':
            return self.get_bs_price()

    def get_mc_price(self):
        """Determine the option price using a Monte Carlo approach"""
        calc = np.zeros([self.iterations, 2])
        rand = np.random.normal(0, 1, [1, self.iterations])
        mult = self.S * np.exp(self.T * (self.r - 0.5 * self.sigma ** 2))

        if self.pc == 'call':
            calc[:, 1] = mult * np.exp(np.sqrt((self.sigma ** 2) * self.T) * rand) - self.K
        elif self.pc == 'put':
            calc[:, 1] = self.K - mult * np.exp(np.sqrt((self.sigma ** 2) * self.T) * rand)

        avg_po = np.sum(np.amax(calc, axis=1)) / float(self.iterations)

        return np.exp(-1.0 * self.r * self.T) * avg_po

    def get_bs_price(self):
        """Determine the option price using the exact Black-Scholes expression."""
        d1 = np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T
        d1 /= self.sigma * np.sqrt(self.T)

        d2 = d1 - self.sigma * np.sqrt(self.T)

        call = self.S * self.ncdf(d1)
        call -= self.K * np.exp(-1.0 * self.r * self.T) * self.ncdf(d2)

        if self.pc == 'call':
            return call
        elif self.pc == 'put':
            return self.apply_pc_parity(call)

    def ncdf(self, x):
        """Cumulative distribution function for the standard normal distribution"""
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    def apply_pc_parity(self, call):
        """Make use of put-call parity to determine put price."""
        return self.K * np.exp(-1.0 * self.r * self.T) - self.S + call
