import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import *
import random
from tkinter import *
import datetime
import db

class Window(Tk):
    def __init__(self, sensor=None):
        super().__init__()

        self.temperature_values = []
        self.min_temperature = 10
        self.max_temperature = 30
        self.date = []

        self.title("Пилипенко Р.О.")
        self.geometry('720x400+400+100')
        self.resizable(width=False, height=False)

        self.figure = plt.Figure(figsize=(2, 2))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().place(x=0, y=0, width=720, height=400)
        self.ax = self.figure.add_subplot(111)

        self.anim = FuncAnimation(self.figure, self.check_values, init_func=None, interval=3000)

    def check_values(self, event):

        new_data = db.get_temperatures(4)

        self.dates = []
        self.temperatures = []

        for instance in new_data:
            self.dates.append(instance[0][5:19])
            self.temperatures.append(instance[1])

        self.update_plot()

    def update_plot(self):
        self.min_temperature, self.max_temperature = db.get_limits()

        self.ax.clear()

        self.ax.plot(self.dates, [self.min_temperature] * len(self.temperatures), color="green")
        self.ax.plot(self.dates, self.temperatures)
        self.ax.plot(self.dates, [self.max_temperature] * len(self.temperatures), color="red")

