import tkinter as tk

class Heatmap:
    def __init__(self, drawing_area, data, min_value=None, max_value=None):
        self.drawing_area = drawing_area
        self.data = data
        self.min_value = min_value if min_value is not None else min(min(row) for row in data)
        self.max_value = max_value if max_value is not None else max(max(row) for row in data)

    def calculate_cell_size(self):
        """Calculate the size of each cell based on the data dimensions."""
        num_rows = len(self.data)
        num_columns = len(self.data[0])
        cell_width = self.drawing_area.width / num_columns
        cell_height = self.drawing_area.height / num_rows
        return cell_width, cell_height

    def get_color(self, value):
        """Get color corresponding to the data value."""
        # Here we are just doing a simple linear interpolation between blue (low) and red (high)
        # You can use more sophisticated color scales like colormap in matplotlib
        relative_value = (value - self.min_value) / (self.max_value - self.min_value)
        red = int(255 * relative_value)
        blue = int(255 * (1 - relative_value))
        green = 0
        return f'#{red:02x}{green:02x}{blue:02x}'

    def draw_cells(self):
        """Draw the cells for the heatmap."""
        cell_width, cell_height = self.calculate_cell_size()
        
        for row_idx, row in enumerate(self.data):
            for col_idx, value in enumerate(row):
                x1 = col_idx * cell_width
                y1 = row_idx * cell_height
                x2 = (col_idx + 1) * cell_width
                y2 = (row_idx + 1) * cell_height
                color = self.get_color(value)
                self.drawing_area.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

    def plot(self):
        """Create a heatmap from the provided data."""
        self.draw_cells()