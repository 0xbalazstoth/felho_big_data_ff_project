class BarChart:
    def __init__(self, drawing_area):
        self.drawing_area = drawing_area

    def calculate_bar_width(self, num_bars):
        """Calculate the width of each bar based on the number of bars."""
        return self.drawing_area.width / (num_bars + 1)

    def normalize_data(self, data):
        """Normalize data values to fit within the canvas height."""
        max_value = max(data.values())
        if max_value == 0: return {k: 0 for k in data}  # Avoid division by zero
        height_factor = (self.drawing_area.height - 20) / max_value  # Leave some space on top
        return {k: v * height_factor for k, v in data.items()}

    def draw_grid(self, num_bars, spacing=50, color="black"):
        """Draw grid lines on the canvas aligned with the bars."""
        bar_width = self.calculate_bar_width(num_bars)
        # Draw vertical grid lines aligned with the bars
        for i in range(num_bars):
            x = (i + 1) * bar_width
            self.drawing_area.canvas.create_line(x, 0, x, self.drawing_area.height, fill=color)
        # Draw horizontal grid lines at regular intervals
        for y in range(spacing, self.drawing_area.height, spacing):
            self.drawing_area.canvas.create_line(0, y, self.drawing_area.width, y, fill=color)

    def plot(self, data, bar_color="blue"):
        """Plot a bar chart using the provided data in key-value format."""
        num_bars = len(data)
        bar_width = self.calculate_bar_width(num_bars)
        normalized_data = self.normalize_data(data)  # Normalize the data
        # Optionally draw the grid first
        self.draw_grid(num_bars)
        for i, (key, value) in enumerate(normalized_data.items()):
            x1 = (i + 0.5) * bar_width
            y1 = self.drawing_area.height - value  # Use normalized value
            x2 = x1 + bar_width / 2
            y2 = self.drawing_area.height
            self.drawing_area.canvas.create_rectangle(x1, y1, x2, y2, fill=bar_color, outline="")
            self.drawing_area.canvas.create_text(x1 + bar_width / 4, y2, anchor="n", text=key)
