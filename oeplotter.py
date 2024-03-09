import random
import tkinter as tk

from plot_interface import PlotInterface
from plots.areachart import AreaChart
from plots.barchart import Barchart
from plots.linechart import LineChart
from plots.piechart import PieChart

groups = [
    {'label': 'Group A', 'values': {'C': 25, 'C++': 15, 'Java': 34, 'Python': 40}},
    {'label': 'Group B', 'values': {'C': 20, 'C++': 10, 'Java': 25, 'Python': 30}},
    {'label': 'Group C', 'values': {'C': 17, 'C++': 7, 'Java': 2, 'Python': 8}},
    {'label': 'Group C', 'values': {'C': 22, 'C++': 5, 'Java': 6, 'Python': 11}}
]

plot_interface = PlotInterface()
barchart = Barchart(plot_interface.canvas)
barchart.add_title("The number of students enrolled in different courses of an institute.")

colors = ['red', 'blue', 'green', 'yellow']
barchart.set_data(groups, colors)

plot_interface.plot(barchart)
plot_interface.show()

# Line chart
# plot_interface2 = PlotInterface()
# linechart = LineChart(plot_interface2.canvas)
# linechart.add_title("The number of students enrolled in different courses of an institute.")

# colors = ['red', 'blue', 'green', 'yellow']
# linechart.set_data(groups, colors)

# plot_interface2.plot(linechart)
# plot_interface2.show()

# AREA CHART
# plot_interface2 = PlotInterface()
# areachart = AreaChart(plot_interface2.canvas)
# areachart.add_title("The number of students enrolled in different courses of an institute.")

# categories = [str(year) for year in range(1990, 2020)]
# generations = ["Generation Z", "Millennials", "Generation X", "Baby Boomers"]
# colors = ['red', 'blue', 'green', 'yellow']

# groups = []
# for gen in generations:
#     values = {cat: random.randint(50, 200) for cat in categories}
#     groups.append({'name': gen, 'values': values})

# areachart.set_data(groups, colors)
# areachart.set_data(groups, colors)

# plot_interface2.plot(areachart)
# plot_interface2.show()

# PIE CHART
# plot_interface2 = PlotInterface()
# piechart = PieChart(plot_interface2.canvas)
# piechart.title_text = "Distribution of Students Across Different Courses"

# def generate_random_color():
#     return f'#{random.randint(0, 0xFFFFFF):06x}'

# data = [random.randint(10, 100) for _ in range(10)]
# labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
# colors = [generate_random_color() for _ in data]
# piechart.set_data(data, labels, colors)
# plot_interface2.plot(piechart)
# plot_interface2.show()