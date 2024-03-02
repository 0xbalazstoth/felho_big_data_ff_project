import tkinter as tk

class TableChart:
    def __init__(self, drawing_area):
        self.drawing_area = drawing_area

    def calculate_cell_size(self, data, num_columns):
        """Calculate the size of each cell based on the data dimensions."""
        num_rows = len(data) + 1  # One for the horizontal header
        cell_width = self.drawing_area.width / num_columns
        cell_height = self.drawing_area.height / num_rows
        return cell_width, cell_height

    def draw_cells(self, data, headers, header_color='#0a4758', cell_color='#007889'):
        """Draw the cells for the table, with headers."""
        num_columns = len(headers['top']) + 1
        cell_width, cell_height = self.calculate_cell_size(data, num_columns)

        # Draw header row
        for i in range(1, num_columns):
            self.drawing_area.canvas.create_rectangle(i * cell_width, 0, (i + 1) * cell_width, cell_height, fill=header_color, outline='')

        # Draw header column
        for i in range(1, len(data) + 1):
            self.drawing_area.canvas.create_rectangle(0, i * cell_height, cell_width, (i + 1) * cell_height, fill=header_color, outline='')

        # Draw data cells
        for i in range(1, len(data) + 1):
            for j in range(1, num_columns):
                self.drawing_area.canvas.create_rectangle(j * cell_width, i * cell_height, (j + 1) * cell_width, (i + 1) * cell_height, fill=cell_color, outline='')

    def populate_cells(self, data, headers, text_color='white'):
        """Fill in the cells with data."""
        num_columns = len(headers['top']) + 1
        cell_width, cell_height = self.calculate_cell_size(data, num_columns)

        # Populate horizontal header
        for col_idx, header in enumerate(headers['top'], start=1):
            x = col_idx * cell_width
            y = cell_height / 2
            self.drawing_area.canvas.create_text(x + cell_width / 2, y, text=header, fill=text_color)

        # Populate vertical header
        for row_idx, header in enumerate(headers['side'], start=1):
            x = cell_width / 2
            y = (row_idx + 1) * cell_height - (cell_height / 2)
            self.drawing_area.canvas.create_text(x, y, text=header, fill=text_color)

        # Populate data cells
        for row_idx, row_data in enumerate(data, start=1):
            for col_idx, value in enumerate(row_data, start=1):
                x = (col_idx + 1) * cell_width - (cell_width / 2)
                y = (row_idx + 1) * cell_height - (cell_height / 2)
                self.drawing_area.canvas.create_text(x, y, text=value, fill=text_color)

    def plot(self, data, headers):
        """Create a table chart from the provided data."""
        self.draw_cells(data, headers)
        self.populate_cells(data, headers)