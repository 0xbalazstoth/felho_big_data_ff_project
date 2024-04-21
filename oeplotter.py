import random
import tkinter as tk
import pandas as pd

from plot_interface import PlotInterface
from plots.barchart import Barchart
from plots.linechart import LineChart

data = pd.read_json("leg.json")

teachers_df = pd.json_normalize(data["data"]["teachers"])

teachers_df['rating_results_avg_rating'] = pd.to_numeric(teachers_df['rating_results_avg_rating'], errors='coerce')
teachers_df = teachers_df.dropna(subset=['rating_results_avg_rating'])

# Preparing data for your custom plotter
groups = [{'label': f"{row['first_name']} {row['last_name']}", 'values': {'Rating': row['rating_results_avg_rating']}} for index, row in teachers_df.iterrows()]
groups = [
    {'label': 'Group A', 'values': {'C': 25, 'C++': 15, 'Java': 34, 'Python': 40}},
    {'label': 'Group B', 'values': {'C': 20, 'C++': 10, 'Java': 25, 'Python': 30}},
    {'label': 'Group C', 'values': {'C': 17, 'C++': 7, 'Java': 2, 'Python': 8}},
    {'label': 'Group C', 'values': {'C': 22, 'C++': 5, 'Java': 6, 'Python': 11}}
]

plot_interface = PlotInterface()
barchart = Barchart(plot_interface.canvas)
barchart.add_title("Programming languages")

colors = ['red', 'blue', 'green', 'yellow']
barchart.set_data(groups, colors)

plot_interface.plot(barchart)
plot_interface.show()

groups = [
    {'label': 'Group A', 'values': {'C': 25, 'C++': 15, 'Java': 34, 'Python': 40}},
    {'label': 'Group B', 'values': {'C': 20, 'C++': 10, 'Java': 25, 'Python': 30}},
    {'label': 'Group C', 'values': {'C': 17, 'C++': 7, 'Java': 2, 'Python': 8}},
    {'label': 'Group C', 'values': {'C': 22, 'C++': 5, 'Java': 6, 'Python': 11}}
]

# Line chart
plot_interface2 = PlotInterface()
linechart = LineChart(plot_interface2.canvas)
linechart.add_title("Programming languages")

colors = ['red', 'blue', 'green', 'yellow']
linechart.set_data(groups, colors)

plot_interface2.plot(linechart)
plot_interface2.show()