import math

class AreaChart:
    def __init__(self, canvas, width=600, height=400):
        self.canvas = canvas
        self.canvas_width = width
        self.canvas_height = height
        self.title_text = None
        self.margin = 70
        self.base_font_size = 14
        self.label_font_size = 10
        self.data = {}
        self.x_labels = []
        self.y_max_value = 10
        self.colors = ["red", "green", "blue", "orange"]

    def on_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.label_font_size = min(max(int(self.base_font_size * (self.canvas_width / 600)), 10), 16)
        self.redraw()

    def calculate_steps(self, max_value):
        magnitude = math.pow(10, math.floor(math.log10(max_value)))
        step = max_value / magnitude / 10
        if step < 1:
            step = 1
        elif step < 2.5:
            step = 2
        elif step < 7.5:
            step = 5
        else:
            step = 10
        step *= magnitude
        return step

    def redraw(self):
        self.canvas.delete("all")

        frame_coords = (self.margin, self.margin, self.canvas_width - self.margin, self.canvas_height - self.margin)
        self.canvas.create_rectangle(*frame_coords, outline="black", width=1)

        if self.title_text:
            self.add_title()

        self.draw_areas()
        self.draw_x_labels()
        self.draw_y_labels()

    def draw_areas(self):
        group_width = (self.canvas_width - 2 * self.margin) / len(self.x_labels)
        for j, group_data in enumerate(self.groups):
            points = [(self.margin, self.canvas_height - self.margin)]
            for i, x_label in enumerate(self.x_labels):
                x = self.margin + group_width * (i + 0.5)
                value = group_data[x_label]
                y = self.canvas_height - self.margin - (value / self.y_max_value * (self.canvas_height - 2 * self.margin))
                points.append((x, y))
            points.append((self.canvas_width - self.margin, self.canvas_height - self.margin))
            self.canvas.create_polygon(points, fill=self.colors[j % len(self.colors)], outline="")

    def draw_x_labels(self):
        num_groups = len(self.groups)
        bar_space = 0.2
        group_space = 1
        total_space = num_groups + bar_space * (num_groups - 1) + group_space
        bar_width = (self.canvas_width - 2 * self.margin) / (len(self.x_labels) * total_space)
        group_width = bar_width * num_groups + bar_space * bar_width * (num_groups - 1)

        for i, label in enumerate(self.x_labels):
            x = self.margin + (group_width + group_space * bar_width) * i + group_width / 2
            y = self.canvas_height - self.margin / 1.5
            self.canvas.create_text(x, y, text=label, fill="black", font=("Arial", self.label_font_size), anchor="n")

    def draw_y_labels(self):
        step = self.calculate_steps(self.y_max_value)
        num_steps = int(self.y_max_value / step)
        step_size = (self.canvas_height - 2 * self.margin) / num_steps
        tick_length = 10
        for i in range(num_steps + 1):
            x = self.margin
            y = self.canvas_height - self.margin - i * step_size
            label = str(int(i * step))
            self.canvas.create_text(x - tick_length * 2, y, text=label, fill="black", font=("Arial", self.label_font_size), anchor="e")
            self.canvas.create_line(x - tick_length, y, x, y, fill="black")

    def add_title(self, title_text=None):
        if title_text:
            self.title_text = title_text
        if self.title_text:
            title_position = (self.canvas_width / 2, self.margin / 3)
            font = ("Arial", self.label_font_size, "bold")
            self.canvas.create_text(title_position, text=self.title_text, fill="black", font=font, anchor="n")

    def set_data(self, groups, colors=None):
        self.groups = [group['values'] for group in groups]
        if colors:
            self.colors = colors
        self.x_labels = list(groups[0]['values'].keys())
        self.y_max_value = max(max(values.values()) for values in self.groups)