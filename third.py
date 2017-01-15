# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from time import time
from math import log, exp, sqrt, pi, pow
from first import Random
from random import Random as PyRandom
from matplotlib import pyplot as plot
from numpy import arange

class BaseRandom(object):
    def __init__(self, n=10000):
        self.intervals = 100
        self.generator = Random.mul_mod_method()
        self._n = n

    def density(self, x):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def stats(self):
        values = [self.next() for _ in xrange(self._n)]
        weights = [10.0 / self._n for _ in xrange(self._n)]
        plot.hist(values, self.intervals, weights=weights, facecolor='g', alpha=0.4)

        x_values = arange(min(values), max(values), 0.001)
        y_values = [self.density(x) for x in x_values]
        plot.plot(x_values, y_values, color='r', lw=1)

        plot.grid(True)
        plot.show()

class ExponentialRandom(BaseRandom):

    def __init__(self, lmbd):
        super(ExponentialRandom, self).__init__()
        self.__lambda = lmbd

    def density(self, x):
        return self.__lambda * exp(0 - self.__lambda * x)

    def next(self):
        x = self.generator.next()
        return 0 - log(1 - x) / self.__lambda

class GaussRandom(BaseRandom):
    def __init__(self, M, sigma, n=12):
        super(GaussRandom, self).__init__()
        self.n = n
        self.M = M
        self.sigma = sigma

    def density(self, x):
        return (1 / (self.sigma * sqrt(2 * pi))) * exp(0 - pow(x - self.M, 2) / 2 * pow(self.sigma, 2))

    def next(self):
        return self.M + self.sigma * sqrt(12 / self.n) * (sum([self.generator.next() for i in range(self.n)]) - self.n / 2)


class TriangularRandom(BaseRandom):
    def __init__(self, a, b):
        super(TriangularRandom, self).__init__()
        self.a = a
        self.b = b

    def density(self, x):
        return 2*(x-self.a) / pow(self.b - self.a, 2)

    def next(self):
        p, q = self.generator.next(), self.generator.next()
        return self.a + (self.b - self.a) * max(p, q)


class SimpsonRandom(BaseRandom):
    def __init__(self, a, b):
        super(SimpsonRandom, self).__init__()
        self.a = a
        self.b = b

    def density(self, x):
        return 2.0 / (self.b - self.a) - 2.0 / pow(self.b -self.a, 2) * abs(self.a + self.b - 2 * x)

    def next(self):
        return self.generator.next() + self.generator.next()


class FunctionRandomTest:


    def test(self):
        ExponentialRandom(1).stats()
        GaussRandom(0, 1).stats()
        TriangularRandom(0, 10).stats()
        SimpsonRandom(0, 2).stats()

if __name__ == '__main__':
    FunctionRandomTest().test()
