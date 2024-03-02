class LineChart:
    def __init__(self, drawing_area):
        self.drawing_area = drawing_area

    def calculate_point_spacing(self, num_points):
        """Calculate the spacing between points based on the number of data points."""
        return self.drawing_area.width / (num_points - 1)

    def normalize_data(self, data):
        """Normalize data values to fit within the canvas height."""
        max_value = max(data.values())
        if max_value == 0: return {k: 0 for k in data}  # Avoid division by zero
        height_factor = (self.drawing_area.height - 20) / max_value  # Leave some space on top
        return {k: v * height_factor for k, v in data.items()}

    def draw_grid(self, num_points, spacing=50, color="black"):
        """Draw grid lines on the canvas."""
        point_spacing = self.calculate_point_spacing(num_points)
        # Draw vertical grid lines at point locations
        for i in range(num_points):
            x = i * point_spacing
            self.drawing_area.canvas.create_line(x, 0, x, self.drawing_area.height, fill=color)
        # Draw horizontal grid lines at regular intervals
        for y in range(spacing, self.drawing_area.height, spacing):
            self.drawing_area.canvas.create_line(0, y, self.drawing_area.width, y, fill=color)

    def plot(self, data, line_color="blue", point_color="red"):
        """Plot a line chart using the provided data in key-value format."""
        num_points = len(data)
        point_spacing = self.calculate_point_spacing(num_points)
        normalized_data = self.normalize_data(data)  # Normalize the data

        # Optionally draw the grid first
        self.draw_grid(num_points)

        # Plot the points and lines
        prev_x = prev_y = None
        for i, (key, value) in enumerate(normalized_data.items()):
            x = i * point_spacing
            y = self.drawing_area.height - value  # Use normalized value

            # Draw the point
            self.drawing_area.canvas.create_oval(x-2, y-2, x+2, y+2, fill=point_color)

            # Draw the line connecting to the previous point
            if prev_x is not None and prev_y is not None:
                self.drawing_area.canvas.create_line(prev_x, prev_y, x, y, fill=line_color)

            prev_x, prev_y = x, y

            # Optionally, you can display the key below each point
            self.drawing_area.canvas.create_text(x, self.drawing_area.height, anchor="n", text=key)
