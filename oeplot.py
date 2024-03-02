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
        bar_width = (self.canvas_width - 2 * self.margin) / (len(self.data) * 2 + 1)
        for i, (label, value) in enumerate(self.data.items()):
            x1 = self.margin + (2 * i + 1) * bar_width
            y1 = self.canvas_height - self.margin
            x2 = x1 + bar_width
            y2 = self.canvas_height - self.margin - (value / self.y_max_value * (self.canvas_height - 2 * self.margin))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

    def draw_x_labels(self):
        bar_width = (self.canvas_width - 2 * self.margin) / (len(self.data) * 2 + 1)    
        label_space = (self.canvas_width - 2 * self.margin) / (len(self.data) * 2 + 1)
        for i, label in enumerate(self.data.keys()):
            x = self.margin + (2 * i + 1) * label_space + bar_width / 2
            y = self.canvas_height - self.margin / 2
            self.canvas.create_text(x, y, text=label, fill="black", font=("Arial", self.label_font_size), anchor="n")

    def draw_y_labels(self):
        # Calculate step values
        step = self.calculate_steps(self.y_max_value)
        num_steps = int(self.y_max_value / step)
        step_size = (self.canvas_height - 2 * self.margin) / num_steps
        tick_length = 10
        for i in range(num_steps + 1):
            x = self.margin
            y = self.canvas_height - self.margin - i * step_size
            label = str(int(i * step))
            self.canvas.create_text(x - tick_length * 2, y, text=label, fill="black", font=("Arial", self.label_font_size), anchor="e")
            # Draw tick on the frame
            self.canvas.create_line(x - tick_length, y, x, y, fill="black")

    def add_title(self, title_text=None):
        if title_text:
            self.title_text = title_text
        if self.title_text:
            title_position = (self.canvas_width / 2, self.margin / 3)
            font = ("Arial", self.label_font_size, "bold")
            self.canvas.create_text(title_position, text=self.title_text, fill="black", font=font, anchor="n")

    def set_data(self, data_dict):
        self.data = data_dict
        self.y_max_value = max(data_dict.values())
        self.x_labels = list(data_dict.keys())

root = tk.Tk()
plot = Plot(root)
plot.add_title("The number of students enrolled in different courses of an institute.")
plot.set_data({'C': 25, 'C++': 15, 'Java': 30, 'Python': 35})
root.mainloop()
