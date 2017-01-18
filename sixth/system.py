from random import expovariate, normalvariate, uniform, triangular, gauss
from generators import simpson
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

        initialize_phases:
            parameters:
                - params:
                    # __phase_1,
                    # __phase_2,
                    # __phase_3,
                    # __phase_4,
                    # __phase_5,
    """

    GENERATORS = {
        'gauss': gauss,
        'expo': expovariate,
        'uniform': uniform,
        'triangular': triangular,
        'simpson': simpson
    }

    # __receiver = Receiver()
    # __phase_5 = Phase(5, partial(simpson, 2, 5), 1, __receiver)
    # __phase_4 = Phase(4, partial(gauss, 5, 1), 4, __phase_5)
    # __phase_3 = Phase(3, partial(triangular, 3, 9), 3, __phase_4)
    # __phase_2 = Phase(1, partial(gauss, 5, 1), 1, __phase_3)
    # __phase_1 = Phase(3, partial(uniform, 3, 9), 5, __phase_2)
    # __source = Sender(__phase_1)

    # __phases = [
        # __source,
        # __phase_1,
        # __phase_2,
        # __phase_3,
        # __phase_4,
        # __phase_5,
        # __receiver
    # ]



    def __init__(self, params, function_draw_callback, function_log_callback):
        self.global_time = 0
        self.__phases = []
        self.function_log_callback = function_log_callback
        self.initialize_phases(params, function_draw_callback, function_log_callback)


    def initialize_phases(self, params, function_draw_callback, function_log_callback):
        self.__receiver = last_phase = Receiver(function_draw_callback, function_log_callback)
        self.__phases.append(self.__receiver)
        params.reverse()
        for phase_params in params:
            phase_params = phase_params + (last_phase, function_log_callback)
            new_phase = Phase(*phase_params)
            self.__phases.append(new_phase)
            last_phase = new_phase

        self.__source = Sender(last_phase, function_log_callback)
        self.__phases.append(self.__source)

    def imitate(self):
        for id, phase in enumerate(self.__phases):
            phase.imitate(self.global_time)

    def start(self, task_count=10000):
        self._task_count = task_count
        while len(self.__receiver.completed) < self._task_count:
            self.imitate()
            self.global_time += GLOBAL_DELTA

    def stats(self):
        for i, phase in enumerate(self.__phases):
            self.function_log_callback("Phase #{}".format(i))
            phase.stats(self.global_time)
            self.function_log_callback('')
        self.function_log_callback('')
