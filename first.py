from matplotlib import pyplot as plot
from matplotlib.figure import Figure
from functools import reduce
from time import time
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from tkinter import *
except:
    from Tkinter import *

def get_moments(selection):
    m = sum(selection) / len(selection)
    D = reduce(lambda x, y: x + y ** 2, selection, 0) / len(selection) - m ** 2
    return m, D


class Random:
    #default values
    z0 = 5920#random.randint(1000,9999)
    M = 2 ** 16
    K = 7 ** 2 * 11 * 13
    A0 = 1

    @staticmethod
    def middle_square_method(start_value=z0):
        current = start_value
        while True:
            yield current / 10000.0
            square = str(current ** 2)
            new_value = ('0' * (8 - len(square)) + square)
            current = int(new_value[2:6])

    @staticmethod
    def mul_mod_method(m=M, k=K, a0=A0):
        a = float((k * a0) % m)
        while True:
            yield a / m
            a = float((k * a) % m)

class Form(object):
    def __init__(self):
        self.root = Tk()
        self.figure = Figure(figsize=(7, 6), dpi=100)
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

    def textaria_add_string(self, textaria, string):
        textaria.insert(END, string)

    def clear(self):
        self.figure.clear()

    def swap_frames(self, frame1, frame2):
        frame1.pack_forget()
        frame2.pack(anchor="w", side=TOP, padx = 5, pady=5)

    def draw(self):
        self.canvas.draw()

    def initialize_form(self):
        raise NotImplementedError

class RandomTest(Form):

    GENERATORS = [
        ("Middle square method", "msm"),
        ("Mul mod method", "mmm"),
    ]

    def __init__(self):
        super(RandomTest, self).__init__()
        self.initialize_form()
        self.show()


    def initialize_form(self):
        self.main_frame = self.add_frame(self.root)
        self.textaria_frame = self.add_frame(self.main_frame)
        self.textaria = self.add_textaria(self.textaria_frame)
        ### header_frame
        self.create_header_frame()
        ### msm_frame
        self.create_msm_frame()
        ### msm_frame
        self.create_mmm_frame()
        self.change_random_generator()

    def create_header_frame(self):
        self.header_frame = self.add_frame(self.main_frame)
        self.radio_value = self.add_radiobuttons(self.header_frame, self.GENERATORS,
            command=self.change_random_generator)
        self.N_textbox = self.add_textbox(self.header_frame, 'Count')
        self.intervals_textbox = self.add_textbox(self.header_frame, 'Intervals')

    def create_msm_frame(self):
        self.msm_frame = self.add_frame(self.main_frame)
        self.z0_textbox = self.add_textbox(self.msm_frame, 'Z0')
        self.button = self.add_button(self.msm_frame, 'submit', command=self.submit)

    def create_mmm_frame(self):
        self.mmm_frame = self.add_frame(self.main_frame)
        self.a0_textbox = self.add_textbox(self.mmm_frame, 'A0')
        self.k_textbox = self.add_textbox(self.mmm_frame, 'K')
        self.m_textbox = self.add_textbox(self.mmm_frame, 'M')
        self.button = self.add_button(self.mmm_frame, 'submit', command=self.submit)

    def change_random_generator(self):
        if self.radio_value.get() == 'mmm':
            self.swap_frames(self.msm_frame, self.mmm_frame)
            self.random_generator = Random.mul_mod_method
        elif self.radio_value.get() == 'msm':
            self.swap_frames(self.mmm_frame, self.msm_frame)
            self.random_generator = Random.middle_square_method


    def submit(self):
        try:
            intervals = int(self.intervals_textbox.get())
            n = int(self.N_textbox.get())
            if self.radio_value.get() == 'msm':
                params = (float(self.z0_textbox.get()),)
            elif self.radio_value.get() == 'mmm':
                params = [
                        float(self.m_textbox.get()),
                        float(self.k_textbox.get()),
                        float(self.a0_textbox.get()),
                    ]
            print(params)
        except:
            raise TypeError
        data = self.test_equality(self.random_generator(*params), intervals, n)
        self.test_independence(self.random_generator(*params), n)
        print(data)
        self.display_data(*data)

    def display_data(self, lefts, related_frequences, intervals):
        self.plot.clear()
        self.plot.bar(lefts, related_frequences, width=(1.0 / intervals))
        self.plot.axhline((1.0/intervals), color='r', linestyle='dashed', linewidth=1)
        max_y = max(related_frequences)
        self.plot.axis([0,1,0,max_y+0.1])
        self.draw()

    def test_equality(self, gen, intervals, n):
        selection = [next(gen) for i in range(n)]
        entries_count = [0] * intervals
        for x in selection:
            entries_count[int(x * intervals)] += 1

        related_frequences = [float(x) / n for x in entries_count]
        lefts = [float(i) / intervals for i in range(intervals)]
        m, D = get_moments(selection)

        string = 'Selection size {},\n M = {},\n D = {}\n'.format(n, round(m, 4), round(D, 4))
        self.textaria_add_string(self.textaria, string)
        return (lefts, related_frequences, intervals)

    def test_independence(self, gen, n):
        s = n / 3
        z = [next(gen) for i in range(n)]

        mx = sum(z) / float(n)
        dx = sum((z[i] - mx) ** 2 for i in xrange(n)) / float(n)
        print(dx)
        mxy = sum(z[i] * z[i + s] for i in xrange(n - s)) / float(n - s)
        r = (mxy - mx * mx) / dx

        string = "R = {}".format(r)
        self.textaria_add_string(self.textaria, string)

if __name__ == '__main__':
    RandomTest()
