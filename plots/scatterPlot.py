class ScatterPlot:
    def __init__(self, drawing_area):
        self.drawing_area = drawing_area

    def normalize_data(self, data):
        """Normalize data points to fit within the canvas dimensions."""
        max_x = max(x for x, _ in data)
        max_y = max(y for _, y in data)
        if max_x == 0: max_x = 1  # Avoid division by zero
        if max_y == 0: max_y = 1
        x_factor = (self.drawing_area.width - 20) / max_x  # Leave some space on sides
        y_factor = (self.drawing_area.height - 20) / max_y  # Leave some space on top
        return [(x * x_factor, self.drawing_area.height - y * y_factor) for x, y in data]

    def draw_grid(self, spacing=50, color="black"):
        """Draw grid lines on the canvas."""
        for x in range(spacing, self.drawing_area.width, spacing):
            self.drawing_area.canvas.create_line(x, 0, x, self.drawing_area.height, fill=color)
        for y in range(spacing, self.drawing_area.height, spacing):
            self.drawing_area.canvas.create_line(0, y, self.drawing_area.width, y, fill=color)

    def plot(self, data, point_color="blue"):
        """Plot a scatter plot using the provided data in (x, y) format."""
        normalized_data = self.normalize_data(data)  # Normalize the data
        self.draw_grid()  # Optionally draw the grid first
        for x, y in normalized_data:
            radius = 3  # Radius of the point
            self.drawing_area.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=point_color, outline="")
