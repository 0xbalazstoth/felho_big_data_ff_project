import random
from area import DrawingArea
from plots.barchart import BarChart
from plots.dotPlot import DotPlot
from plots.heatmap import Heatmap
from plots.lineChart import LineChart
from plots.scatterPlot import ScatterPlot
from plots.stemPlot import StemPlot
from plots.tableChart import TableChart

drawing_area = DrawingArea()
bar_chart = BarChart(drawing_area)
data = {"A": 100, "B": 200, "C": 150, "D": 300, "E": 250, "F": 300, "G": 50, "H": 300, "I": 1100, "J": 560, "O": 1546}
bar_chart.plot(data, bar_color="green")
drawing_area.show()

# drawing_area2 = DrawingArea()
# line_chart = LineChart(drawing_area2)
# line_chart.plot(data, line_color="green")
# drawing_area2.show()

# drawing_area3 = DrawingArea()
# stem_plot = StemPlot(drawing_area3)
# stem_plot.plot(data)
# drawing_area3.show()

# drawing_area4 = DrawingArea()
# data4 = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(100)]
# scatter_plot = ScatterPlot(drawing_area4)
# scatter_plot.plot(data4)
# drawing_area4.show()

# drawing_area5 = DrawingArea()
# dot_plot = DotPlot(drawing_area5)
# dot_plot.plot(data)
# drawing_area5.show()

# drawing_area6 = DrawingArea()
# table_chart = TableChart(drawing_area6)
# headers = {
#     'top': ['1', '2', '3'],
#     'side': ['A', 'B', 'C', 'D']
# }
# data6 = [
#     ['30', '50', '20'],
#     ['60', '10', '70'],
#     ['40', '90', '80'],
#     ['20', '9', '83']
# ]
# table_chart.plot(data6, headers)
# drawing_area6.show()

# drawing_area7 = DrawingArea()
# data7 = [
#     [30, 50, 20],
#     [60, 10, 70],
#     [40, 90, 80],
#     [40, 90, 80],
# ]
# heatmap = Heatmap(drawing_area7, data7)
# heatmap.plot()
# drawing_area7.show()