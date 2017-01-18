# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from first import Random
from matplotlib import pyplot as plot
from matplotlib.figure import Figure
from functools import reduce
from time import time
# import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from tkinter import *
except:
    from Tkinter import *



class Form(object):
    def __init__(self):
        self.root = Tk()
        self.figure = Figure(figsize=(7, 7), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas._tkcanvas.pack(side=LEFT)
        self.canvas.show()

    def show(self):
        self.root.mainloop()

    def add_frame(self, master):
        frame = Frame(master)
        frame.pack(side=TOP, anchor="w",  padx = 5)
        return frame

    def add_textbox(self, master, title):
        label = Label(master, text=title, anchor=W, font='Arial 13')
        label.pack(fill=BOTH, pady = 5)
        entry = Entry(master, font='Arial 14')
        entry.pack()
        return entry

    def add_button(self, master, title, command=None):
        button = Button(master, text='submit', command=command)
        button.pack(pady = 5)
        return button

    def add_radiobuttons(self, master, modes, command=None):
        radio_value = StringVar()
        radio_value.set(modes[0][1])
        for text, mode in modes:
            radio = Radiobutton(master, text=text, command=command,
                variable=radio_value, value=mode, font='Arial 12' )
            radio.pack(anchor=W)
        return radio_value

    def add_textaria(self, master):
        textaria = Text(master, width=30, height=10, font='Arial 10',wrap=WORD)
        textaria.pack(side=TOP, fill=BOTH, pady=5)
        return textaria

    def textaria_add_string(self, string):
        self.textaria.insert(END, string)

    def clear(self):
        self.figure.clear()

    def swap_frames(self, frame1, frame2):
        frame1.pack_forget()
        frame2.pack(anchor="w", side=TOP, padx = 5, pady=5)

    def draw(self):
        self.canvas.draw()

    def initialize_form(self):
        raise NotImplementedError

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

class CustomForm(Form):
    GENERATORS = [
        ("Simple event", "s"),
        ("Complex event", "c"),
        ("Complex dependent event", "cd"),
        ("Complex group event", "cg"),
    ]

    def __init__(self):
        super(CustomForm, self).__init__()
        self.initialize_form()
        self.show()

    def initialize_form(self):
        self.main_frame = self.add_frame(self.root)
        self.textaria_frame = self.add_frame(self.main_frame)
        self.textaria = self.add_textaria(self.textaria_frame)
        ### header_frame
        self.create_header_frame()
        #create frames
        self.event_frames = {}
        self.event_frames['s'] = self.create_s_frame()
        self.event_frames['c'] = self.create_c_frame()
        self.event_frames['cd'] = self.create_cd_frame()
        self.event_frames['cg'] = self.create_cg_frame()

        self.change_random_generator()

    def create_header_frame(self):
        self.header_frame = self.add_frame(self.main_frame)
        self.radio_value = self.add_radiobuttons(self.header_frame, self.GENERATORS,
            command=self.change_random_generator)
        self.N_textbox = self.add_textbox(self.header_frame, 'Count')
        # self.intervals_textbox = self.add_textbox(self.header_frame, 'Intervals')

    def create_s_frame(self):
        self.s_frame = self.add_frame(self.main_frame)
        self.s_pa_textbox = self.add_textbox(self.s_frame, 'P(a):')
        self.s_button = self.add_button(self.s_frame, 'submit', command=self.submit)
        return self.s_frame

    def create_c_frame(self):
        self.c_frame = self.add_frame(self.main_frame)
        self.c_pa_textbox = self.add_textbox(self.c_frame, 'P(a):')
        self.c_pb_textbox = self.add_textbox(self.c_frame, 'P(b):')
        self.c_button = self.add_button(self.c_frame, 'submit', command=self.submit)
        return self.c_frame

    def create_cd_frame(self):
        self.cd_frame = self.add_frame(self.main_frame)
        self.cd_pa_textbox = self.add_textbox(self.cd_frame, 'P(a):')
        self.cd_pb_textbox = self.add_textbox(self.cd_frame, 'P(b):')
        self.cd_pba_textbox = self.add_textbox(self.cd_frame, 'P(b/a):')
        self.cd_button = self.add_button(self.cd_frame, 'submit', command=self.submit)
        return self.cd_frame

    def create_cg_frame(self):
        self.cg_frame = self.add_frame(self.main_frame)
        self.cg_pg_textbox = self.add_textbox(self.cg_frame, 'P(group):')
        self.button = self.add_button(self.cg_frame, 'submit', command=self.submit)
        return self.cg_frame

    def change_random_generator(self):
        if self.radio_value.get() == 'c':
            self.swap_frames('c')
        elif self.radio_value.get() == 's':
            self.swap_frames('s')
        elif self.radio_value.get() == 'cd':
            self.swap_frames('cd')
        elif self.radio_value.get() == 'cg':
            self.swap_frames('cg')

    def swap_frames(self, key):

        keys = set(self.event_frames.keys()) - set([key])
        for k in keys:
            self.event_frames[k].pack_forget()
        self.event_frames[key].pack(side=TOP, anchor="w",  padx = 5)

    def submit(self):
        try:
            # intervals = int(self.intervals_textbox.get())
            n = int(self.N_textbox.get())

            if self.radio_value.get() == 's':
                params = [
                    float(self.s_pa_textbox.get()),
                    n,
                ]
                function = self.test_simple_event
            elif self.radio_value.get() == 'c':
                params = [
                    float(self.c_pb_textbox.get()),
                    float(self.c_pa_textbox.get()),
                    n,
                ]
                function = self.test_complex_event

            elif self.radio_value.get() == 'cd':
                params = [
                    float(self.cd_pa_textbox.get()),
                    float(self.cd_pb_textbox.get()),
                    float(self.cd_pba_textbox.get()),
                    n,
                ]
                function = self.test_complex_dependent_event

            elif self.radio_value.get() == 'cg':
                values = []
                print(self.cg_pg_textbox.get().replace(' ','').split(','))
                for i in self.cg_pg_textbox.get().replace(' ','').split(','):
                    values.append(float(i))
                if (abs(sum(values) - 1) > 0.001):
                    self.textaria_add_string('Event does not present a full group.')
                    return
                params = [values, n]
                function = self.test_complete_group_event

        except:
            raise TypeError

        function(*params)


class RandomEventsTest(CustomForm):
    # iterations = [10, 100, 1000, 10000]
    # random_generator = Random.mul_mod_method()

    def test_simple_event(self, p_a, n):
        # p_a = cls.random_generator.next()
        class_event = SimpleRandomEvent(p_a)
        self.textaria_add_string('Teoretical probability (P(A) -> {})\n\n'.format(p_a))
        # for n in cls.iterations:
        p = sum(1.0 / n for i in xrange(n) if class_event.imitate())
        self.textaria_add_string("n = {:6}:\n P(A) = {}\n\n".format(n, p))

    def test_complex_event(self, p_a, p_b, n):
        # p_a = cls.random_generator.next()
        # p_b = cls.random_generator.next()
        class_event = ComplexRandomEvent(p_a, p_b)
        self.textaria_add_string('Teoretical probability (P(A) -> {},\n P(B) -> {})\n\n'.format(p_a, p_b))
        # for n in cls.iterations:
        pa = 0
        pb = 0
        for i in xrange(n):
            a, b = class_event.imitate()
            pa += float(a) / n
            pb += float(b) / n
        self.textaria_add_string("n = {:6}:\n P(A) -> {},\n P(B) -> {}\n\n".format(n, pa, pb))

    def test_complex_dependent_event(self, p_a, p_b, p_ba, n):
        # p_a = cls.random_generator.next()
        # p_b = cls.random_generator.next()
        # p_ba = cls.random_generator.next()
        class_event = ComplexDependentRandomEvent(p_a, p_b, p_ba)
        self.textaria_add_string('Teoretical probability (P(A) -> {:.5f},\n P(B) -> {:.5f},\n P(B/A) -> {:.5f})\n\n'.format(p_a, p_b, p_ba))
        # for n in cls.iterations:
        pa = 0
        pb = 0
        pba = 0
        for i in xrange(n):
            a, b = class_event.imitate()
            pa += float(a) / n
            pb += float(b) / n
            pba += float(a and b) / n
        self.textaria_add_string("n = {}:\n P(A) = {:.5f},\n P(B) -> {:.5f},\n P(B/A) -> {:.5f}\n\n".format(n, pa, pb, pba / pa, 4))

    def test_complete_group_event(self, p_array, n):
        # p_array = [0.2, 0.1, 0.05, 0.35, 0.2, 0.07, 0.03]
        self.textaria_add_string('Teoretical probability (P(group) -> {}\n\n'.format(p_array))
        class_event = CompleteGroupRandomEvent(p_array)
        # for n in cls.iterations:
        p = [class_event.imitate() for _ in xrange(n)]
        self.plot.clear()
        bins = self.plot.hist(p, len(p_array), weights=[1.0 / n for i in xrange(n)])
        max_y = max(bins[0])
        self.plot.axis([0,len(p_array) - 1,0,max_y+0.1])
        self.textaria_add_string('n = {}:\n P -> {}\n\n'.format(n, bins[0]))
        self.draw()

        # plot.show()


    def test(self):
        print('test_simple_event:')
        self.test_simple_event()
        print('\n\ntest_complex_event:')
        self.test_complex_event()
        print('\n\ntest_complex_dependent_event:')
        self.test_complex_dependent_event()
        self.test_complete_group_event()

if __name__ == '__main__':
    RandomEventsTest()#.test()
