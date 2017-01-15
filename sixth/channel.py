from constants import *
from unit import Unit


class Channel(Unit):
    def __init__(self,tag, distribution_generator):
        super(Channel, self).__init__(tag)
        self._generator = distribution_generator

    def