import math
from lab1 import brv_gen


def exponential(lamda=2, rand=brv_gen(25325)):
    def generator(l, rand):
        while True:
            yield round(-math.log(rand.next()) / l, 2)
    return generator(lamda, rand).next


def gauss(m=0, sigma=1, rand=brv_gen(34632)):
    def generator(m, sigma, rand):
        while True:
            yield round(m + sigma * (sum([rand.next() for _ in xrange(12)]) - 6), 2)
    return generator(m, sigma, rand).next


def triangular(a=0, b=2, rand=brv_gen(68434)):
    def generator(a,b,rand):
        while True:
            yield round(a+(b-a)*max(rand.next(), rand.next()), 2)
    return generator(a,b,rand).next


def simpson(a=0, b=2, rand1=brv_gen(83349), rand2=brv_gen(115535)):
    def generator(a, b, rand, rand2):
        while True:
            yield round(rand.next() + rand2.next(), 2)
    return generator(a,b,rand1, rand2).next


def uniform(a=0, b=2, rand=brv_gen(94567)):
    def generator(a, b, rand):
        while True:
            yield round(rand.next()*(b-a) + a, 2)
    return generator(a, b, rand).next

