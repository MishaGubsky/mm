from globals import *

class Queue:

    def __init__(self, capacity):
        self._capacity = capacity
        if self._capacity > 0:
            self._status = AVAILABLE
        else:
            self._status = BUSY
        self._tasks = []

    @property
    def capacity(self):
        return self._capacity

    @property
    def tasks(self):
        return self._tasks

    @property
    def size(self):
        return len(self._tasks)

    @property
    def is_empty(self):
        return len(self._tasks) == 0

    @property
    def is_available(self):
        return self._status == AVAILABLE

    def add_task(self, task):
        if len(self._tasks) >= self._capacity:
            import pdb; pdb.set_trace();

            raise 'Queue is overflow'
        self._tasks.append(task)
        if len(self._tasks) >= self._capacity:
            self._status = BUSY

    def pop(self):
        if len(self._tasks) < self._capacity:
            self._status = AVAILABLE
        if not self.is_empty:
            return self.tasks.pop()
        else:
            return None
