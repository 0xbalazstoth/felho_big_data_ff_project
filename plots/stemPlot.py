class StemPlot:
    def __init__(self, drawing_area):
        self.drawing_area = drawing_area

    def normalize_data(self, data):
        max_value = max(data.values())
        if max_value == 0: return {k: 0 for k in data}
        height_factor = (self.drawing_area.height - 20) / max_value
        return {k: v * height_factor for k, v in data.items()}

    def draw_grid(self, num_stems, spacing=50, color="black"):
        stem_spacing = self.drawing_area.width / (num_stems + 1)
        for i in range(num_stems):
            x = (i + 1) * stem_spacing
            self.drawing_area.canvas.create_line(x, 0, x, self.drawing_area.height, fill=color)
        for y in range(spacing, self.drawing_area.height, spacing):
            self.drawing_area.canvas.create_line(0, y, self.drawing_area.width, y, fill=color)

    def plot(self, data, stem_color="blue", marker="o", line_width=2):
        num_stems = len(data)
        stem_spacing = self.drawing_area.width / (num_stems + 1)
        normalized_data = self.normalize_data(data)
        self.draw_grid(num_stems)

        for i, (key, value) in enumerate(normalized_data.items()):
            x = (i + 1) * stem_spacing
            y = self.drawing_area.height - value
            # Draw the stem with increased width
            self.drawing_area.canvas.create_line(x, self.drawing_area.height, x, y, fill=stem_color, width=line_width)
            if marker == "o":
                self.drawing_area.canvas.create_oval(x-4, y-4, x+4, y+4, fill=stem_color, outline="")
            self.drawing_area.canvas.create_text(x, self.drawing_area.height + 10, anchor="n", text=key)
