from constants import *
from unit import Unit


class Queue(Unit):

    def __init__(self, tag, capacity, discard_if_full):
        super(Queue, self).__init__(tag)
        self._capacity = capacity
        self._status = AVAILABLE
        self._requests = []

    @property
    def capacity(self):
        return self._capacity

    @property
    def requests(self):
        return self._requests

    @property
    def size(self):
        return len(self._requests)

    def receive_request(self, r):
        self._requests.append(r)
        if len(self._requests) >=self._capacity:
            self._status = BUSY

    def try_send_request(self, dst_unit):
        if dst_unit.is_available():
            dst_unit.take_request(self._requests[0])
            self._requests.__delitem__(0)
            return True
        return False
