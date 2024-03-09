import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, IntVar
from PIL import Image

class PlotInterface:
    def __init__(self, width=800, height=600, bg="white", title="Data Visualization Tool", min_width=800, min_height=800):
        self.width = width
        self.height = height
        self.bg = bg
        self.title = title
        self.min_width = min_width
        self.min_height = min_height

        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.minsize(self.min_width, self.min_height)

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, bg=self.bg)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind mouse events to drawing methods
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.last_x, self.last_y = None, None  # Initialize last recorded coordinates

        self.save_button = tk.Button(self.frame, text="Save as PNG", command=self.open_save_dialog)
        self.save_button.pack(side=tk.BOTTOM, pady=10)

        self.chart = None

    def plot(self, chart):
        """Attach a chart or plot to the interface."""
        self.chart = chart
        self.canvas.bind("<Configure>", self.chart.on_resize)
        self.chart.redraw()

    def clear(self):
        """Clear the canvas."""
        self.canvas.delete("all")

    def show(self):
        """Show the Tkinter window with the canvas."""
        self.root.mainloop()
        
    def start_draw(self, event):
        """Record the starting point for drawing."""
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        """Draw a line from the last point to the current point."""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black")
            self.last_x, self.last_y = event.x, event.y

    def stop_draw(self, event):
        """Reset the last recorded coordinates on mouse release."""
        self.last_x, self.last_y = None, None

    def open_save_dialog(self):
        """Open a modal-like dialog window for saving options."""
        self.dialog = Toplevel(self.root)
        self.dialog.title("Save Options")
        
        # Set a fixed width and height for the dialog window
        dialog_width = 200
        dialog_height = 150
        center_x = int(self.root.winfo_x() + (self.root.winfo_width() / 2) - (dialog_width / 2))
        center_y = int(self.root.winfo_y() + (self.root.winfo_height() / 2) - (dialog_height / 2))

        # Set the position of the dialog window to be centered relative to the main window
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")
        self.dialog.resizable(False, False)

        self.color_option = IntVar(value=1)  # Default to colorized

        colorize_button = tk.Radiobutton(self.dialog, text="Colorized", variable=self.color_option, value=1)
        colorize_button.pack()

        grayscale_button = tk.Radiobutton(self.dialog, text="Grayscale", variable=self.color_option, value=0)
        grayscale_button.pack()

        save_button = tk.Button(self.dialog, text="Save", command=self.save_to_png)
        save_button.pack(pady=10)

    def save_to_png(self):
        """Save the current canvas to a PNG file with an option for colorized or grayscale."""
        self.dialog.destroy()  # Close the dialog

        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if not file_path:
            return

        ps_file = file_path + '.ps'

        colormode = 'color' if self.color_option.get() else 'gray'
        self.canvas.postscript(file=ps_file, colormode=colormode)

        try:
            image = Image.open(ps_file)
            image.load(scale=10)
            if not self.color_option.get():  # If grayscale is selected, convert the image
                image = image.convert('L')
            image.save(file_path, 'PNG', quality=95)
        except Exception as e:
            messagebox.showerror("Error Saving Image", str(e))
        finally:
            import os
            os.remove(ps_file)
