from globals import *

class Task(object):

    def __init__(self, global_time):
        self.t = None
        self.received = None
        self.created = global_time
