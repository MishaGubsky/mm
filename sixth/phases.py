from random import expovariate, normalvariate, uniform, triangular
from queue import Queue
from channel import Channel
from task import Task
from globals import *
from matplotlib import pyplot as plot

class Phase:

    def __init__(self, channels_count, generator, queue_length, next_phase):
        self._queue_length = queue_length
        self._random = generator
        self._next = next_phase
        self._channels = [Channel(self._random)] * channels_count
        self._queue = Queue(queue_length)
        self.queue_lengths = []
        self.states = [[0, 0, 0] for _ in xrange(channels_count)]

    def _update_times(self):
        for channel in self._channels:
            if channel.is_available:
                continue
            need_to_retrive = channel.update()
            if need_to_retrive:
                added = self._next.add_task(channel.task)
                if added:
                    channel.free()
                else:
                    channel.block()


    def _send_tasks(self):
        for channel in self._channels:
            if not channel.is_available and not self._queue.is_empty:
                channel.add_task(self._queue.pop())

    def _update_stats(self):
        self.queue_lengths.append(self._queue.size)
        for i, channel in enumerate(self._channels):
            if not channel.is_blocked:
                self.states[i][0] += 1
            elif channel.is_available:
                self.states[i][1] += 1
            else:
                self.states[i][2] += 1

    def add_task(self, task):
        free_channel_not_exist = all(not channel.is_available for channel in self._channels)
        if not self._queue.is_available and free_channel_not_exist:
            return False

        if not free_channel_not_exist:
            for channel in self._channels:
                if channel.is_available:
                    channel.add_task(task)
                    return True
        self._queue.add_task(task)
        return True

    def imitate(self):
        self._update_times()
        self._send_tasks()
        self._update_stats()

    def stats(self):
        avg_queue_l = sum(self.queue_lengths) / float(len(self.queue_lengths))
        print "average queue length = {}".format(avg_queue_l)

        import pdb; pdb.set_trace();

        iterations = GLOBAL_TIME / GLOBAL_DELTA
        msg = "P of states:"
        for i, state in enumerate(self.states):
            blocked_p = state[0] / iterations
            free_p = state[1] / iterations
            worked_p = state[2] / iterations
            msg = "#{}: blocked: {:.5}, free = {:.5}, processing = {:.5}"
            print msg.format(i, blocked_p, free_p, worked_p)


class Sender:

    def __init__(self, next_phase):
        self._next = next_phase
        self._next_task = 0
        self.rejected = []
        self.total = 0

    def add_task(self, task):
        pass

    def imitate(self):
        self._next_task -= GLOBAL_DELTA
        if self._next_task <= 0:
            self.total += 1
            self._next_task = expovariate(1)
            task = Task()
            added = self._next.add_task(task)
            if not added:
                self.rejected.append(task)

    def stats(self):
        reject_p = len(self.rejected) / float(self.total)
        print "P of rejection: {:.5}".format(reject_p)


class Receiver:

    def __init__(self):
        self.completed = []

    def add_task(self, task):
        task.received = GLOBAL_TIME
        self.completed.append(task)
        return True

    def imitate(self):
        pass

    def stats(self):
        completed = self.completed
        intervals = []
        for i in xrange(1, len(completed)):
            intervals.append(abs(completed[i].received - completed[i - 1].received))
        plot.hist(intervals, bins=50)
        plot.show()

        e = sum(intervals) / float(len(intervals))
        d = sum(((i - e) ** 2) for i in intervals) / len(intervals)
        print "Mo intervals between orders: {:.5}".format(e)
        print "D intervals between orders: {:.5}".format(d)

        process_times = [t.received - t.created for t in completed]
        plot.hist(process_times, bins=50)
        plot.show()

        e = sum(process_times) / len(process_times)
        d = sum(((i - e) ** 2) for i in process_times) / len(process_times)
        print "Mo order processing time: {:.5}".format(e)
        print "D order processing time: {:.5}".format(d)
