# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from random import random
from first import Random
from matplotlib import pyplot as plot


class RandomEvent(object):

    def __init__(self):
        self.random_generator = Random.mul_mod_method()

    def random(self):
        return self.random_generator.next()

    def imitate(self):
        raise  NotImplementedError


class SimpleRandomEvent(RandomEvent):

    def __init__(self, p):
        super(SimpleRandomEvent, self).__init__()
        self._p = p

    def imitate(self):
        x = self.random()
        return x <= self._p


class ComplexRandomEvent(RandomEvent):

    def __init__(self, pa, pb):
        super(ComplexRandomEvent, self).__init__()
        self._pa = pa
        self._pb = pb

    def imitate(self):
        x1 = self.random()
        x2 = self.random()
        a = x1 <= self._pa
        b = x2 <= self._pb
        return a, b


class ComplexDependentRandomEvent(RandomEvent):

    def __init__(self, pa, pb, pba):
        super(ComplexDependentRandomEvent, self).__init__()
        self._pa = pa
        self._pb = pb
        self._pba = pba
        self._pbna = (pb - pba * pa) / (1 - pa)

    def imitate(self):
        x1 = self.random()
        x2 = self.random()
        a = (x1 <= self._pa)
        b = (a and (x2 <= self._pba)) or (not a and (x2 <= self._pbna))
        return a, b


class CompleteGroupRandomEvent(RandomEvent):

    def __init__(self, p):
        super(CompleteGroupRandomEvent, self).__init__()

        if abs(1 - sum(p)) > 1e-4:
            raise ValueError('It is not collective exhaustive events.')
        self._p = p

    def imitate(self):
        x = self.random()
        k = 0
        while x > sum(self._p[:k]):
            k += 1
        return k - 1


class RandomEventsTest:
    iterations = [10, 100, 1000, 10000]
    random_generator = Random.mul_mod_method()

    @classmethod
    def test_simple_event(cls):
        p_a = cls.random_generator.next()
        class_event = SimpleRandomEvent(p_a)
        print('Teoretical probability (P(A) -> {})'.format(p_a))
        for n in cls.iterations:
            p = sum(1.0 / n for i in xrange(n) if class_event.imitate())
            print "n = {:6}: P(A) = {}".format(n, p)

    @classmethod
    def test_complex_event(cls):
        p_a = cls.random_generator.next()
        p_b = cls.random_generator.next()
        class_event = ComplexRandomEvent(p_a, p_b)
        print('Teoretical probability (P(A) -> {}, P(B) -> {})'.format(p_a, p_b))
        for n in cls.iterations:
            pa = 0
            pb = 0
            for i in xrange(n):
                a, b = class_event.imitate()
                pa += float(a) / n
                pb += float(b) / n
            print "n = {:6}: P(A) = {}, P(B) -> {}".format(n, pa, pb)

    @classmethod
    def test_complex_dependent_event(cls):
        p_a = cls.random_generator.next()
        p_b = cls.random_generator.next()
        p_ba = cls.random_generator.next()
        class_event = ComplexDependentRandomEvent(p_a, p_b, p_ba)
        print('Teoretical probability (P(A) -> {:.5f}, P(B) -> {:.5f}, P(B/A) -> {:.5f})'.format(p_a, p_b, p_ba))
        for n in cls.iterations:
            pa = 0
            pb = 0
            pba = 0
            for i in xrange(n):
                a, b = class_event.imitate()
                pa += float(a) / n
                pb += float(b) / n
                pba += float(a and b) / n
            print("n = {}: P(A) = {:.5f}, P(B) -> {:.5f}, P(B/A) -> {:.5f}".format(n, pa, pb, pba / pa, 4))

    @classmethod
    def test_complete_group_event(cls):
        p_array = [0.2, 0.1, 0.05, 0.35, 0.2, 0.07, 0.03]
        class_event = CompleteGroupRandomEvent(p_array)
        for n in cls.iterations:
            p = [class_event.imitate() for _ in xrange(n)]
            bins = plot.hist(p, len(p_array), weights=[1.0 / n for i in xrange(n)])
            plot.axis([0,len(p_array) - 1,0, 0.5])
            plot.title('n = {}: P -> {}'.format(n, bins[0]))
            plot.show()


    @classmethod
    def test(cls):
        print('test_simple_event:')
        cls.test_simple_event()
        print('\n\ntest_complex_event:')
        cls.test_complex_event()
        print('\n\ntest_complex_dependent_event:')
        cls.test_complex_dependent_event()
        cls.test_complete_group_event()

if __name__ == '__main__':
    RandomEventsTest.test()
