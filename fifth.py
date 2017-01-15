import numpy as np
from first import Random
import matplotlib.pyplot as plot
from collections import OrderedDict


class BaseRandom(object):

    _distribution = None

    def __init__(self, n=10000):
        self.intervals = 10
        self.generator = Random.mul_mod_method()
        self._n = n

    def next(self):
        raise NotImplementedError

    def stats(self):
        values = [self.next() for _ in xrange(self._n)]
        weights = [10.0 / self._n for _ in xrange(self._n)]
        plot.hist(values, self.intervals, weights=weights, facecolor='g', alpha=0.4)
        #
        # values = [self.next() for _ in xrange(self._n)]
        # weights = [1.0 / self._n for _ in xrange(self._n)]
        # plot.hist(values, self.intervals, weights=weights, facecolor='g', alpha=0.7)

        # x_values = self._distribution.keys()
        # y_values = [self._distribution.values()[0]]
        # for i in xrange(1, len(self._distribution.values())):
        #     y_values.append(self._distribution.values()[i] - self._distribution.values()[i - 1])
        # plot.plot(x_values, y_values, color='b', lw=1, alpha=0.7, marker='.', markeredgewidth=5)

        plot.grid(True)
        plot.show()


class SystemValuesRandom(BaseRandom):

    _distribution = OrderedDict((
        (1.0, 0.125),
        (1.3, 0.165),
        (2.3, 0.325),
        (2.9, 0.5),
        (3.6, 0.51),
        (4.1, 0.59),
        (4.3, 0.62),
        (4.7, 0.66),
        (5.9, 0.74),
        (7.0, 0.88),
        (8.4, 0.94),
        (10.0, 1.0),
    ))

    def __init__(self, X_values, Y_values, XY_probabilities):
        super(SystemValuesRandom, self).__init__()
        self.X_values = X_values
        self.Y_values = Y_values
        self.XY_probabilities = XY_probabilities

    # def next(self):
    #     # X_probabilities = np.sum(self.XY_probabilities, axis=1)
    #     x = self.generator.next()
    #     for i in range(len(X_probabilities)):
    #         if x <= np.sum(X_probabilities[0:i + 1]):
    #             break
    #
    #     y = self.generator.next() * X_probabilities[i]
    #     Y_probabilities = self.XY_probabilities[i, :]
    #     for j in range(len(Y_probabilities)):
    #         if y <= np.sum(Y_probabilities[0:j + 1]):
    #             break
    #
    #     return i, j

    # def next(self):
    #     x = self.generator.next()
    #     for y, p in self._distribution.iteritems():
    #         if x < p:
    #             return y



if __name__ == "__main__":
    # n = 10**6
    X_values = [0.5, 0.7, 0.4, 0.6]
    Y_values = [2.6, 1.3, 5.7, 6.4]
    # XY_probabilities = np.array([
    #     [0.1, 0.1, 0.05],
    #     [0.07, 0.09, 0.09],
    #     [0.2, 0.09, 0.01],
    #     [0.06, 0.08, 0.06],
    # ], dtype=float)
    # system_gen = SystemValuesRandom(X_values, Y_values, XY_probabilities)
    # XY_practical = np.zeros((len(X_values), len(Y_values)))
    # cells = [system_gen.next() for i in range(n)]
    # for cell in cells:
    #     XY_practical[cell] += 1
    # print(XY_practical*1./n)
    # print(np.sum(XY_practical)*1./n)
    SystemValuesRandom(X_values, Y_values).stats()
