import tkinter as tk

class DrawingArea:
    def __init__(self, width=800, height=600, bg="white", title="Data Visualization Tool"):
        self.width = width
        self.height = height
        self.bg = bg
        self.title = title

        self.root = tk.Tk()
        self.root.title(self.title)

        # Create the Canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.bg)
        self.canvas.pack()

    def clear(self):
        """Clear the canvas."""
        self.canvas.delete("all")

    def show(self):
        """Show the Tkinter window with the canvas."""
        self.root.mainloop()