from random import normalvariate, uniform, triangular
from phases import *
from functools import partial
from globals import *

class System:
    """
        Phase(channels_count, generator, queue_length, next_phase)
        Sender(next_phase)
        generators:
            triangular: low, high, mode
            uniform: a, b
            normalvariate: mu, sigma
            expovariate: lambda
            gauss: mu, sigma
    """
    __receiver = Receiver()
    __phase_5 = Phase(5, partial(triangular, 2, 5, 3.5), 3, __receiver)
    __phase_4 = Phase(3, partial(uniform, 3, 9), 3, __phase_5)
    __phase_3 = Phase(4, partial(normalvariate, 5, 1), 3, __phase_4)
    __phase_2 = Phase(4, partial(normalvariate, 5, 2), 0, __phase_3)
    __phase_1 = Phase(3, partial(uniform, 3, 9), 3, __phase_2)
    __source = Sender(__phase_1)

    __phases = [
        __source,
        __phase_1,
        __phase_2,
        __phase_3,
        __phase_4,
        __phase_5,
        __receiver
    ]

    def __init__(self, task_count=10000):
        self._task_count = task_count

    def imitate(self):
        for phase in self.__phases:
            phase.imitate()

    def start(self):
        GLOBAL_TIME = 0
        while len(self.__receiver.completed) < self._task_count:
            self.imitate()
            GLOBAL_TIME += GLOBAL_DELTA

    def stats(self):
        for i, phase in enumerate(self.__phases):
            print "Phase #{}".format(i)
            phase.stats()
            print
