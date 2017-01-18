# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from system import System
from matplotlib import pyplot as plot
from numpy import arange
from matplotlib.figure import Figure
from functools import partial
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
        self.figure.subplots_adjust(hspace=.5)
        self.plot = self.figure.add_subplot(211)
        self.plot.set_title('dsdds')
        self.plot1 = self.figure.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas._tkcanvas.grid(row=0, column=0, rowspan=4)
        self.canvas.show()

        # row=0, column=0, rowspan=2

    def show(self):
        self.root.mainloop()

    def add_frame(self, master):
        return Frame(master)

    def add_textbox(self, master, title):
        label = Label(master, text=title, anchor=W, font='Arial 13')
        label.pack( pady = 5)
        entry = Entry(master, font='Arial 14')
        entry.pack(side=TOP)
        return entry

    def add_label(self, master, title):
        label = Label(master, text=title, anchor=W, font='Arial 13')
        label.pack(fill=BOTH, padx = 5, )
        return label

    def add_button(self, master, title, side, command=None):
        button = Button(master, text=title, width=6,height=2, command=command)
        button.pack(side=side, pady = 5)
        return button

    def add_radiobuttons(self, master, modes, command=None):
        radio_value = StringVar()
        radio_value.set(modes[0][1])
        for text, mode in modes:
            radio = Radiobutton(master, text=text, command=command,
            variable=radio_value, value=mode, font='Arial 12' )
            radio.pack(anchor=W)
        return radio_value

    def textaria_add_string(self, string):
        string += '\n'
        self.log_textaria.insert(END, string)

    def clear(self):
        self.figure.clear()

    def draw(self):
        self.canvas.draw()

    def initialize_form(self):
        raise NotImplementedError

class CustomForm(Form):

    def __init__(self):
        super(CustomForm, self).__init__()
        self.initialize_form()
        self.show()

    def initialize_form(self):
        main_frame = self.add_frame(self.root)
        main_frame.grid(row=0, column=1, columnspan=3)


        frame_container = self.add_frame(main_frame)
        frame_container.grid(row=0, column=1)
        self.phases_textaria = self.add_textaria_frame(frame_container, LEFT,'Phases', 20, 10)
        self.channel_textaria = self.add_textaria_frame(frame_container, RIGHT,'Ch', 5, 10)
        self.capacities_textaria = self.add_textaria_frame(frame_container, RIGHT,'L', 5, 10)


        button_frame = self.add_frame(main_frame)
        button_frame.grid(row=1, column=1)
        self.task_count_textbox = self.add_textbox(button_frame, 'Task count:')
        self.add_button(button_frame, 'imitate', TOP, command=self.submit)

        textaria_frame = self.add_frame(main_frame)
        textaria_frame.grid(row=2, column=1, columnspan=2, rowspan=2)
        self.log_textaria = self.add_textaria(textaria_frame, 40, 24, TOP)

    def add_textaria_frame(self, master, side, text, width, height):
        frame = self.add_frame(master)
        frame.pack(side=LEFT)
        self.add_label(frame,text)
        textaria = self.add_textaria(frame, width, height, LEFT)
        textaria.pack(side=side, pady=5, padx=5)
        return textaria

    def add_textaria(self, master, width, height, side):
        textaria = Text(master, width=width, height=height, font='Arial 10',wrap=WORD)
        textaria.pack(side=side, pady=5, padx=5)
        return textaria

    def submit(self):
        try:
            task_count = int(self.task_count_textbox.get())
            params = self.parse_phases()
        except:
            raise TypeError

        smp = System(params, self.display_data, self.textaria_add_string)
        smp.start(task_count=task_count)
        smp.stats()

    def parse_phases(self):
        generators = self.parse_generators(self.phases_textaria.get('1.0', END))
        chanels = self.get_int_list(self.channel_textaria.get('1.0', END))
        capacities = self.get_int_list(self.capacities_textaria.get('1.0', END))

        try:
            params = zip(chanels, generators, capacities)
            return params
        except:
            raise ValueError

    def get_int_list(self, text):
        string_list = filter(None, text.split('\n'))
        valid_ints = []
        try:
            for s in string_list:
                valid_ints.append(int(s.replace(' ','').replace('\t', '')))
            return valid_ints
        except:
            raise TypeError

    def parse_generators(self, text):
        generators = filter(None, text.split('\n'))
        valid_generators = []
        try:
            for p in generators:
                params = p.replace(' ','').replace('\t', '').split(',')
                generator = self.get_generator(params[0])
                valid_params = self.parse_params(params[1:])
                valid_generators.append(partial(generator, *valid_params))
            return valid_generators
        except:
            raise TypeError

    def get_generator(self, generator_text):
        if generator_text in System.GENERATORS.keys():
            return System.GENERATORS[generator_text]
        else:
            raise ValueError

    def parse_params(self, params):
        valid_params = []
        try:
            for p in params:
                valid_params.append(float(p))
            return valid_params
        except:
            raise TypeError

    def display_data(self, intervals_params, process_times_params):
        self.plot.clear()
        self.plot1.clear()

        self.plot.hist(intervals_params[0], bins=50)
        self.plot.set_title('Intervals between orders, M = {}, D = {}'.format(round(intervals_params[1], 4), round(intervals_params[2], 4)))

        self.plot1.hist(process_times_params[0], bins=50)
        self.plot1.set_title('Order processing time: M = {}, D = {}'.format(round(process_times_params[1], 4), round(process_times_params[2], 4)))

        self.draw()


if __name__ == '__main__':
    CustomForm()
    # system = System(1000)
    # system.start()
    # system.stats()
