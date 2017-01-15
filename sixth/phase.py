from queue import Queue

class Phase(object):

    def __init__(self, queue_capacity):
        self._queue = Queue(queue_capacity,)