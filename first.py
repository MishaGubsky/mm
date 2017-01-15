from matplotlib import pyplot as plot
from functools import reduce
from time import time
import random

def get_moments(selection):
    m = sum(selection) / len(selection)
    D = reduce(lambda x, y: x + y ** 2, selection, 0) / len(selection) - m ** 2
    return m, D


class Random:
    #default values
    z0 = 5920#random.randint(1000,9999)
    M = 2 ** 16
    K = 7 ** 2 * 11 * 13
    A0 = 1

    @staticmethod
    def middle_square_method(start_value=z0):
        current = start_value
        while True:
            yield current / 10000.0
            square = str(current ** 2)
            new_value = ('0' * (8 - len(square)) + square)
            current = int(new_value[2:6])

    @staticmethod
    def mul_mod_method(m=M, k=K, a0=A0):
        a = float((k * a0) % m)
        while True:
            yield a / m
            a = float((k * a) % m)


class RandomTest:
    Intervals = 20
    N = 100

    def __init__(self, random_generator):
        self.random_generator = random_generator

    @classmethod
    def test_equality(cls, gen, intervals, n):
        selection = [next(gen) for i in range(n)]
        entries_count = [0] * intervals
        for x in selection:
            entries_count[int(x * intervals)] += 1

        print(entries_count)
        related_frequences = [float(x) / n for x in entries_count]
        lefts = [float(i) / intervals for i in range(intervals)]

        m, D = get_moments(selection)

        plot.bar(lefts, related_frequences, width=(1.0 / intervals))
        # plot.hist(selection, intervals, weights=[1.0 / n for i in xrange(n)])
        plot.axhline((1.0/intervals), color='r', linestyle='dashed', linewidth=1)
        plot.xlabel('Quantity')
        plot.xlabel('Intervals')
        plot.axis([0,1,0,1.01])
        plot.title('Selection size {}, M = {}, D = {}'.format(n, round(m, 4), round(D, 4)))
        plot.show()

    @classmethod
    def test_independence(cls, gen, n):
        s = n / 3
        z = [next(gen) for i in range(n)]

        mx = sum(z) / float(n)
        dx = sum((z[i] - mx) ** 2 for i in xrange(n)) / float(n)
        print(dx)
        mxy = sum(z[i] * z[i + s] for i in xrange(n - s)) / float(n - s)
        r = (mxy - mx * mx) / dx
        print("Selection size {}, R = {}".format(len(z), r))

    def test(self):
        self.test_equality(self.random_generator, self.Intervals, self.N)
        self.test_independence(self.random_generator, self.N)


if __name__ == '__main__':
    msm_generator = Random.middle_square_method()
    mmm_generator = Random.mul_mod_method()

    print('middle_square_method test:')
    RandomTest(msm_generator).test()
    print('mul_mod_method test:')
    RandomTest(mmm_generator).test()
