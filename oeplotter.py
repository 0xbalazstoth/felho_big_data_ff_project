import tkinter as tk

from plot_interface import PlotInterface
from plots.barchart import Barchart
from plots.linechart import LineChart

groups = [
    {'label': 'Group A', 'values': {'C': 25, 'C++': 15, 'Java': 34, 'Python': 40}},
    {'label': 'Group B', 'values': {'C': 20, 'C++': 10, 'Java': 25, 'Python': 30}},
    {'label': 'Group C', 'values': {'C': 17, 'C++': 7, 'Java': 2, 'Python': 8}},
    {'label': 'Group C', 'values': {'C': 22, 'C++': 5, 'Java': 6, 'Python': 11}}
]

# plot_interface = PlotInterface()
# barchart = Barchart(plot_interface.canvas)
# barchart.add_title("The number of students enrolled in different courses of an institute.")

# colors = ['red', 'blue', 'green', 'yellow']
# barchart.set_data(groups, colors)

# plot_interface.plot(barchart)
# plot_interface.show()

# Line chart
plot_interface2 = PlotInterface()
linechart = LineChart(plot_interface2.canvas)
linechart.add_title("The number of students enrolled in different courses of an institute.")

colors = ['red', 'blue', 'green', 'yellow']
linechart.set_data(groups, colors)

plot_interface2.plot(linechart)
plot_interface2.show()