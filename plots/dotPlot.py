class DotPlot:
    def __init__(self, drawing_area):
        self.drawing_area = drawing_area

    def calculate_dot_spacing(self, num_dots):
        """Calculate the spacing between dots based on the number of dots."""
        return self.drawing_area.width / (num_dots + 1)

    def normalize_data(self, data):
        """Normalize data values to fit within the canvas height."""
        max_value = max(data.values())
        if max_value == 0: return {k: 0 for k in data}  # Avoid division by zero
        height_factor = (self.drawing_area.height - 20) / max_value  # Leave some space on top
        return {k: v * height_factor for k, v in data.items()}

    def draw_grid(self, num_dots, spacing=50, color="black"):
        """Draw grid lines on the canvas for reference."""
        dot_spacing = self.calculate_dot_spacing(num_dots)
        # Draw vertical grid lines at the dot positions
        for i in range(num_dots):
            x = (i + 1) * dot_spacing
            self.drawing_area.canvas.create_line(x, 0, x, self.drawing_area.height, fill=color)
        # Draw horizontal grid lines at regular intervals
        for y in range(spacing, self.drawing_area.height, spacing):
            self.drawing_area.canvas.create_line(0, y, self.drawing_area.width, y, fill=color)

    def plot(self, data, dot_color="red", dot_size=5):
        """Plot a dot plot using the provided data in key-value format."""
        num_dots = len(data)
        dot_spacing = self.calculate_dot_spacing(num_dots)
        normalized_data = self.normalize_data(data)  # Normalize the data
        # Optionally draw the grid first
        self.draw_grid(num_dots)
        for i, (key, value) in enumerate(normalized_data.items()):
            x = (i + 1) * dot_spacing
            y = self.drawing_area.height - value  # Use normalized value
            # Draw the dot
            self.drawing_area.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill=dot_color, outline="")
            # Label below the dot
            self.drawing_area.canvas.create_text(x, self.drawing_area.height - 5, text=key, anchor="n")
