import math

class LineChart:
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

        self.draw_lines()
        self.draw_x_labels()
        self.draw_y_labels()
        
    def draw_x_labels(self):
        group_width = (self.canvas_width - 2 * self.margin) / len(self.x_labels)
        for i, label in enumerate(self.x_labels):
            x = self.margin + group_width * (i + 0.5)
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

    def draw_lines(self):
        group_width = (self.canvas_width - 2 * self.margin) / len(self.x_labels)
        for j, group_data in enumerate(self.groups):
            previous_x = previous_y = None
            for i, x_label in enumerate(self.x_labels):
                x = self.margin + group_width * (i + 0.5)
                value = group_data[x_label]
                y = self.canvas_height - self.margin - (value / self.y_max_value * (self.canvas_height - 2 * self.margin))
                if previous_x is not None and previous_y is not None:
                    self.canvas.create_line(previous_x, previous_y, x, y, fill=self.colors[j % len(self.colors)], width=2)
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=self.colors[j % len(self.colors)], outline="")
                previous_x, previous_y = x, y

    def set_data(self, groups, colors=None):
        self.groups = [group['values'] for group in groups]
        if colors:
            self.colors = colors
        self.x_labels = list(groups[0]['values'].keys())
        self.y_max_value = max(max(values.values()) for values in self.groups)
