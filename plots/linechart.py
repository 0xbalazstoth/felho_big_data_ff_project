import math
from tkinter.font import Font

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
        # Estimate a reasonable number of divisions on the y-axis
        ideal_steps = 10  # or another number that gives a good balance

        # Initial step calculation based on the max_value
        raw_step = max_value / ideal_steps
        magnitude = math.pow(10, math.floor(math.log10(raw_step)))
        step = round(raw_step / magnitude) * magnitude

        # Make sure the steps are not too granular
        if step < 1:
            step = round(step, 1)
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
        self.draw_legend()
        
    def draw_legend(self):
        legend_font = Font(family="Arial", size=self.label_font_size)
        legend_x_start = self.margin
        legend_y = self.canvas_height - self.margin / 6
        box_width = 20
        box_height = 10
        spacing = 10

        for legend_label, color in zip(self.legend_labels, self.colors):
            self.canvas.create_rectangle(legend_x_start, legend_y - box_height, legend_x_start + box_width, legend_y, fill=color, outline=color)
            self.canvas.create_text(legend_x_start + box_width + spacing, legend_y - box_height / 2, text=legend_label, anchor='w', fill="black")
            text_width = legend_font.measure(legend_label)
            legend_x_start += box_width + text_width + 2 * spacing
        
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

        # Determine the number of decimal places to display
        decimal_places = 0 if step.is_integer() else len(str(step).split('.')[1])

        for i in range(num_steps + 1):
            x = self.margin
            y = self.canvas_height - self.margin - i * step_size
            label_value = i * step
            # Format label with appropriate number of decimal places
            label_format = "{:." + str(decimal_places) + "f}"
            label = label_format.format(label_value)
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
        self.legend_labels = [group['label'] for group in groups]
        self.x_labels = list(groups[0]['values'].keys())
        self.y_max_value = max(max(values.values()) for values in self.groups)
