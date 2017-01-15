import numpy as np
from first import Random
import matplotlib.pyplot as plot
from collections import OrderedDict
from mpl_toolkits.mplot3d import Axes3D

class BaseRandom(object):

    _distribution = None

    def __init__(self, n=10000):
        self.intervals = 10
        self.generator = Random.mul_mod_method()
        self._n = n

    def next(self):
        raise NotImplementedError

    def stats(self):
        x, y = [], []
        for i in xrange(self._n):
            values = self.next()
            x.append(values[0])
            y.append(values[1])

        XY_practical = np.zeros((len(X_values), len(Y_values)))
        cells = [system_generator.next() for i in range(self._n)]
        for cell in cells:
            XY_practical[cell] += 1

        x_pos = []
        y_pos = []
        dz = []
        for _ in xrange(len(self.X_values)):
            for _1 in xrange(len(self.Y_values)):
                x_pos.append(_)
                y_pos.append(_1)
                dz.append(XY_practical[_,_1]/self._n)
        z_pos = np.zeros_like(x_pos)


        fig = plot.figure()
        ax = fig.add_subplot(111, projection='3d')

        dx = 0.3 * np.ones_like(z_pos)
        dy = dx.copy()
        # dz = hist.flatten()
        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color='b', zsort='average', alpha=0.8)
        # ax.bar3d(x_pos, y_pos, z_pos, dx, dy, [5,7,4], color='b', zsort='average', alpha=0.8)
        plot.show()


class SystemValuesRandom(BaseRandom):

    def __init__(self, X_values, Y_values, XY_probabilities):
        super(SystemValuesRandom, self).__init__()
        self.X_values = X_values
        self.Y_values = Y_values
        self.XY_probabilities = XY_probabilities

    def next(self):
        X_probabilities = np.sum(self.XY_probabilities, axis=1)
        x = self.generator.next()
        for i in range(len(X_probabilities)):
            if x <= np.sum(X_probabilities[0:i + 1]):
                break

        y = self.generator.next() * X_probabilities[i]
        Y_probabilities = self.XY_probabilities[i, :]
        for j in range(len(Y_probabilities)):
            if y <= np.sum(Y_probabilities[0:j + 1]):
                break

        return i, j


if __name__ == "__main__":
    n=10000
    X_values = [0.1, 0.2, 0.1, 0.05, 0.15, 0.25, 0.15]
    Y_values = [2.6, 1.3, 5.7]
    XY_probabilities = np.array([
        [0.1, 0.07, 0.04],
        [0.07, 0.07, 0.04],
        [0.04, 0.04, 0.04],
        [0.03, 0.05, 0.04],
        [0.04, 0.05, 0.03],
        [0.05, 0.04, 0.04],
        [0.05, 0.03, 0.03],
    ], dtype=float)
    system_generator = SystemValuesRandom(X_values, Y_values, XY_probabilities)
    XY_practical = np.zeros((len(X_values), len(Y_values)))
    cells = [system_generator.next() for i in range(n)]
    for cell in cells:
        XY_practical[cell] += 1
    print(XY_practical*1./n)
    print(np.sum(XY_practical)*1./n)

    system_generator.stats()
