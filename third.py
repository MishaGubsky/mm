# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from time import time
from math import log, exp, sqrt, pi, pow
from first import Random
from random import Random as PyRandom
from matplotlib import pyplot as plot
from numpy import arange
from matplotlib.figure import Figure
from functools import reduce
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from tkinter import *
except:
    from Tkinter import *



class Form(object):
    def __init__(self):
        self.root = Tk()
        self.figure = Figure(figsize=(7, 7), dpi=100)
        self.plot1 = self.figure.add_subplot(111)
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
        frame2.pack(side=TOP, anchor="w",  padx = 5)

    def draw(self):
        self.canvas.draw()

    def initialize_form(self):
        raise NotImplementedError

class BaseRandom(object):
    def __init__(self, n=10000):
        self.intervals = 100
        self.generator = Random.mul_mod_method()
        self._n = n

    def density(self, x):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def stats(self, n=10000, intervals=100, plot=plot):
        values = [self.next() for _ in xrange(n)]
        weights = [10.0 / n for _ in xrange(n)]
        # plot.hist(values, intervals, weights=weights, facecolor='g', alpha=0.4)

        x_values = arange(min(values), max(values), 0.001)
        y_values = [self.density(x) for x in x_values]

        return ((values, intervals, weights),(x_values, y_values))
        # plot.plot(x_values, y_values, color='r', lw=1)
        #
        # plot.grid(True)
        # plot.show()

class ExponentialRandom(BaseRandom):

    def __init__(self, lmbd):
        super(ExponentialRandom, self).__init__()
        self.__lambda = lmbd

    def density(self, x):
        return self.__lambda * exp(0 - self.__lambda * x)

    def next(self):
        x = self.generator.next()
        return 0 - log(1 - x) / self.__lambda

class GaussRandom(BaseRandom):
    def __init__(self, M, sigma, n=12):
        super(GaussRandom, self).__init__()
        self.n = n
        self.M = M
        self.sigma = sigma

    def density(self, x):
        return (1 / (self.sigma * sqrt(2 * pi))) * exp(0 - pow(x - self.M, 2) / 2 * pow(self.sigma, 2))

    def next(self):
        return self.M + self.sigma * sqrt(12 / self.n) * (sum([self.generator.next() for i in range(self.n)]) - self.n / 2)

class TriangularRandom(BaseRandom):
    def __init__(self, a, b):
        super(TriangularRandom, self).__init__()
        self.a = a
        self.b = b

    def density(self, x):
        return 2*(x-self.a) / pow(self.b - self.a, 2)

    def next(self):
        p, q = self.generator.next(), self.generator.next()
        return self.a + (self.b - self.a) * max(p, q)

class SimpsonRandom(BaseRandom):
    def __init__(self, a, b):
        super(SimpsonRandom, self).__init__()
        self.a = a
        self.b = b

    def density(self, x):
        return 2.0 / (self.b - self.a) - 2.0 / pow(self.b -self.a, 2) * abs(self.a + self.b - 2 * x)

    def next(self):
        return self.generator.next() + self.generator.next()

class CustomForm(Form):
    GENERATORS = [
        ("Exponential", "e"),
        ("Gauss", "g"),
        ("Triangular", "t"),
        ("Simpson", "s"),
    ]

    def __init__(self):
        super(CustomForm, self).__init__()
        self.initialize_form()
        self.show()

    def initialize_form(self):
        self.main_frame = self.add_frame(self.root)
        # self.textaria_frame = self.add_frame(self.main_frame)
        # self.textaria = self.add_textaria(self.header_frame)

        ### header_frame
        self.create_header_frame()
        #create frames
        self.event_frames = {}
        self.event_frames['e'] = self.create_e_frame()
        self.event_frames['g'] = self.create_g_frame()
        self.event_frames['t'] = self.create_t_frame()
        self.event_frames['s'] = self.create_s_frame()

        self.change_random_generator()

    def create_header_frame(self):
        self.header_frame = self.add_frame(self.main_frame)
        self.textaria = self.add_textaria(self.header_frame)
        self.radio_value = self.add_radiobuttons(self.header_frame, self.GENERATORS,
            command=self.change_random_generator)
        self.N_textbox = self.add_textbox(self.header_frame, 'Count')
        self.intervals_textbox = self.add_textbox(self.header_frame, 'Intervals')

    def create_e_frame(self):
        self.e_frame = self.add_frame(self.main_frame)
        self.e_textbox = self.add_textbox(self.e_frame, 'Lambda:')
        self.button = self.add_button(self.e_frame, 'submit', command=self.submit)
        return self.e_frame

    def create_g_frame(self):
        self.g_frame = self.add_frame(self.main_frame)
        self.g_mu_textbox = self.add_textbox(self.g_frame, 'Mu:')
        self.g_sigma_textbox = self.add_textbox(self.g_frame, 'Sigma:')
        self.button = self.add_button(self.g_frame, 'submit', command=self.submit)
        return self.g_frame

    def create_s_frame(self):
        self.s_frame = self.add_frame(self.main_frame)
        self.s_a_textbox = self.add_textbox(self.s_frame, 'A:')
        self.s_b_textbox = self.add_textbox(self.s_frame, 'B:')
        self.s_button = self.add_button(self.s_frame, 'submit', command=self.submit)
        return self.s_frame

    def create_t_frame(self):
        self.t_frame = self.add_frame(self.main_frame)
        self.t_a_textbox = self.add_textbox(self.t_frame, 'A:')
        self.t_b_textbox = self.add_textbox(self.t_frame, 'B:')
        self.t_button = self.add_button(self.t_frame, 'submit', command=self.submit)
        return self.t_frame

    def change_random_generator(self):
        if self.radio_value.get() == 'e':
            self.swap_frames('e')
        elif self.radio_value.get() == 'g':
            self.swap_frames('g')
        elif self.radio_value.get() == 't':
            self.swap_frames('t')
        elif self.radio_value.get() == 's':
            self.swap_frames('s')

    def swap_frames(self, key):

        keys = set(self.event_frames.keys()) - set([key])
        for k in keys:
            self.event_frames[k].pack_forget()
        self.event_frames[key].pack(side=TOP, anchor="w",  padx = 5)

    def submit(self):
        try:
            intervals = int(self.intervals_textbox.get())
            n = int(self.N_textbox.get())

            if self.radio_value.get() == 'e':
                params = [
                    float(self.e_textbox.get()),
                ]
                law = ExponentialRandom
            elif self.radio_value.get() == 'g':
                params = [
                    float(self.g_mu_textbox.get()),
                    float(self.g_sigma_textbox.get()),
                ]
                law = GaussRandom

            elif self.radio_value.get() == 't':
                params = [
                    float(self.t_a_textbox.get()),
                    float(self.t_b_textbox.get()),
                ]
                law = TriangularRandom

            elif self.radio_value.get() == 's':
                params = [
                    float(self.s_a_textbox.get()),
                    float(self.s_b_textbox.get()),
                ]
                law = SimpsonRandom
        except:
            raise TypeError

        data = law(*params).stats(n, intervals)
        self.display_data(*data)


        # data = self.test_equality(self.random_generator(*params), intervals, n)
        # self.test_independence(self.random_generator(*params), n)
        # print(data)
        # self.display_data(*data)

    def display_data(self, hist_params, plot_params):
        self.plot.clear()
        # self.plot.bar(lefts, related_frequences, width=(1.0 / intervals))
        # self.plot.axhline((1.0/intervals), color='r', linestyle='dashed', linewidth=1)
        # max_y = max(related_frequences)
        # self.plot.axis([0,1,0,max_y+0.1])

        self.plot.hist(hist_params[0], hist_params[1], weights=hist_params[2], facecolor='g', alpha=0.4)
        self.plot.plot(plot_params[0], plot_params[1], color='r', lw=1)

        # plot.grid(True)
        # plot.show()

        self.draw()

class FunctionRandomTest(CustomForm):
    def test(self):
        pass
    #     ExponentialRandom(1).stats()
    #     GaussRandom(0, 1).stats()
    #     TriangularRandom(0, 10).stats()
    #     SimpsonRandom(0, 2).stats()

if __name__ == '__main__':
    FunctionRandomTest()
