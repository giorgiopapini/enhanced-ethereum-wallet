from tkinter import *

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime


class BasicChart:

    def __init__(self, master=None, data=None, kind=None, color=None, title=None, font_size=7.5):

        self.master = master
        self.data = data
        self.kind = kind
        self.color = color
        self.title = title
        self.font_size = font_size

    def place_chart(self):
        x = [val[0] for val in self.data]
        y = [val[1] for val in self.data]
        data = {"Time": x, "Value": y}
        df = DataFrame(data, columns=["Time", "Value"])
        figure = plt.Figure(figsize=(3.9, 2.32), dpi=100, constrained_layout=True)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self.master)
        line.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df = df[["Time", "Value"]].groupby("Time").sum()
        df.plot(kind=self.kind, legend=True, ax=ax, color=self.color, fontsize=self.font_size)

        updated_xticks = [datetime.fromtimestamp(int(str(int(time))[:-3])).strftime('%d-%m-%y') for time in
                          ax.get_xticks()]
        ax.set_xticklabels(updated_xticks, rotation=15)  # rotation=45
        ax.set_xlabel(None)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        ax.set_title(self.title, pad=17, loc="left")
