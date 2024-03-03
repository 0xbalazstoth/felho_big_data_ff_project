import math
import tkinter as tk

class Plot:
    def __init__(self, root, title="Responsive Chart Frame", width=600, height=400):
        self.root = root
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        self.canvas_width = width
        self.canvas_height = height
        self.title_text = None
        self.margin = 70
        self.base_font_size = 14
        self.label_font_size = 10
        self.data = {}
        self.x_labels = []
        self.y_max_value = 10

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

        self.draw_bars()
        self.draw_x_labels()
        self.draw_y_labels()

    def draw_bars(self):
        num_groups = len(self.groups)
        bar_space = 0.2  # Space between bars within a group
        group_space = 1  # Space between groups
        total_space = num_groups + bar_space * (num_groups - 1) + group_space
        bar_width = (self.canvas_width - 2 * self.margin) / (len(self.x_labels) * total_space)
        group_width = bar_width * num_groups + bar_space * bar_width * (num_groups - 1)

        for i, x_label in enumerate(self.x_labels):
            for j, group_data in enumerate(self.groups):
                x1 = self.margin + (group_width + group_space * bar_width) * i + (bar_width + bar_space * bar_width) * j
                y1 = self.canvas_height - self.margin
                value = group_data[x_label]
                x2 = x1 + bar_width
                y2 = self.canvas_height - self.margin - (value / self.y_max_value * (self.canvas_height - 2 * self.margin))
                color_index = j % len(self.colors)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors[color_index], width=0)

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
        self.groups = [group['values'] for group in groups]  # Extract just the values from the groups
        self.colors = colors or ["red", "green", "blue", "orange"]
        self.x_labels = list(groups[0]['values'].keys())
        self.y_max_value = max(max(values.values()) for values in self.groups)

root = tk.Tk()
plot = Plot(root)
plot.add_title("The number of students enrolled in different courses of an institute.")
groups = [
    {'label': 'Group A', 'values': {'C': 25, 'C++': 15, 'Java': 30, 'Python': 35}},
    {'label': 'Group B', 'values': {'C': 20, 'C++': 10, 'Java': 25, 'Python': 30}},
    {'label': 'Group C', 'values': {'C': 17, 'C++': 7, 'Java': 2, 'Python': 8}},
    {'label': 'Group C', 'values': {'C': 22, 'C++': 5, 'Java': 6, 'Python': 11}}
]

# Optional colors for the bars
colors = ['red', 'blue', 'green', 'yellow']
plot.set_data(groups, colors)
root.mainloop()
