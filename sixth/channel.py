from globals import *

class Channel:
    def __init__(self, distribution_generator):
        self._random = distribution_generator
        self._status = AVAILABLE
        self._task = None

    @property
    def is_available(self):
        return self._status == AVAILABLE

    @property
    def is_blocked(self):
        return self._status == BLOCKED

    @property
    def is_available(self):
        return self._status == AVAILABLE

    @property
    def task(self):
        return self._task

    def free(self):
        task = self._task
        self._task = None
        self._status = AVAILABLE

    def add_task(self, task):
        task.t = self._random()
        self._task = task
        self._status = BUSY

    def block(self):
        self._status = BLOCKED

    def update(self):
        if self._task:
            self._task.t = self._task.t - GLOBAL_DELTA
            if self._task.t <= 0:
                return True
        return False
