import tkinter as tk

from plot_interface import PlotInterface
from plots.barchart import Barchart

plot_interface = PlotInterface()
barchart = Barchart(plot_interface.canvas)
barchart.add_title("The number of students enrolled in different courses of an institute.")
groups = [
    {'label': 'Group A', 'values': {'C': 25, 'C++': 15, 'Java': 30, 'Python': 35}},
    {'label': 'Group B', 'values': {'C': 20, 'C++': 10, 'Java': 25, 'Python': 30}},
    {'label': 'Group C', 'values': {'C': 17, 'C++': 7, 'Java': 2, 'Python': 8}},
    {'label': 'Group C', 'values': {'C': 22, 'C++': 5, 'Java': 6, 'Python': 11}}
]

colors = ['red', 'blue', 'green', 'yellow']
barchart.set_data(groups, colors)

plot_interface.plot(barchart)
plot_interface.show()