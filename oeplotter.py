import random
import tkinter as tk

from plot_interface import PlotInterface
from plots.areachart import AreaChart
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
# plot_interface2 = PlotInterface()
# linechart = LineChart(plot_interface2.canvas)
# linechart.add_title("The number of students enrolled in different courses of an institute.")

# colors = ['red', 'blue', 'green', 'yellow']
# linechart.set_data(groups, colors)

# plot_interface2.plot(linechart)
# plot_interface2.show()

plot_interface2 = PlotInterface()
areachart = AreaChart(plot_interface2.canvas)  # Step 1: Instantiate AreaChart
areachart.add_title("The number of students enrolled in different courses of an institute.")  # Step 2: Add a title

categories = [str(year) for year in range(1990, 2020)]

# Define generations
generations = ["Generation Z", "Millennials", "Generation X", "Baby Boomers"]

# Colors for each generation
colors = ['red', 'blue', 'green', 'yellow']

# Generate random data for each generation across the defined categories
groups = []
for gen in generations:
    values = {cat: random.randint(50, 200) for cat in categories}  # Random values between 50 and 200
    groups.append({'name': gen, 'values': values})

areachart.set_data(groups, colors)
areachart.set_data(groups, colors)  # Step 3: Set data and colors

plot_interface2.plot(areachart)
plot_interface2.show()