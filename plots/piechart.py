import math

class PieChart:
    def __init__(self, canvas, width=600, height=400):
        self.canvas = canvas
        self.canvas_width = width
        self.canvas_height = height
        self.title_text = None
        self.margin = 70
        self.base_font_size = 14
        self.label_font_size = 10
        self.data = []
        self.labels = []
        self.colors = ["red", "green", "blue", "orange"]

    def set_data(self, data, labels=None, colors=None):
        self.data = data
        self.labels = labels if labels else [''] * len(data)
        if colors:
            self.colors = colors
        self.redraw()
        
    def on_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.label_font_size = min(max(int(self.base_font_size * (self.canvas_width / 600)), 10), 16)
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        self.draw_pie()
        if self.title_text:
            self.add_title()

    def draw_pie(self):
        total = sum(self.data)
        start_angle = -90  # Starting from the top
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        radius = min(self.canvas_width - 2 * self.margin, self.canvas_height - 2 * self.margin) / 2

        for i, value in enumerate(self.data):
            extent = 360 * value / total  # Calculate the slice size
            end_angle = start_angle + extent
            mid_angle = start_angle + extent / 2  # Midpoint angle for the label
            color = self.colors[i % len(self.colors)]  # Cycle through colors

            # Create the slice
            self.canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                start=start_angle, extent=extent, fill=color, outline="")

            # Draw label line ('tick')
            tick_length = 20  # Length of the tick from the edge of the pie
            tick_inner_x = center_x + radius * math.cos(math.radians(mid_angle))
            tick_inner_y = center_y + radius * math.sin(math.radians(mid_angle))
            tick_outer_x = center_x + (radius + tick_length) * math.cos(math.radians(mid_angle))
            tick_outer_y = center_y + (radius + tick_length) * math.sin(math.radians(mid_angle))
            self.canvas.create_line(tick_inner_x, tick_inner_y, tick_outer_x, tick_outer_y, fill="black")

            # Determine label position based on the angle
            label_x_offset = 30  # Adjust as needed for your specific chart size
            if -90 <= mid_angle <= 90:
                # Right side
                anchor = "w"
                label_x = tick_outer_x + label_x_offset
            else:
                # Left side
                anchor = "e"
                label_x = tick_outer_x - label_x_offset

            label_y = tick_outer_y

            # Draw label text
            self.canvas.create_text(label_x, label_y, text=self.labels[i], anchor=anchor, fill="black",
                                    font=("Arial", self.label_font_size))

            start_angle = end_angle  # Prepare for the next slice



    def add_title(self):
        if self.title_text:
            title_position = (self.canvas_width / 2, self.margin / 3)
            font = ("Arial", self.label_font_size, "bold")
            self.canvas.create_text(title_position, text=self.title_text, fill="black", font=font, anchor="n")