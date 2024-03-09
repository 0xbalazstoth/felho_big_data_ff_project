import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, IntVar, colorchooser
from PIL import Image

class PlotInterface:
    def __init__(self, width=800, height=600, bg="white", title="Data Visualization Tool", min_width=800, min_height=800):
        self.width = width
        self.height = height
        self.bg = bg
        self.title = title
        self.min_width = min_width
        self.min_height = min_height

        self.drawing_color = "black"

        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.minsize(self.min_width, self.min_height)

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, bg=self.bg)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Pencil tool setup
        self.pencil_button = tk.Button(self.frame, text="Pencil", command=self.use_pencil)
        self.pencil_button.pack(side=tk.LEFT)

        # Eraser tool setup
        self.eraser_button = tk.Button(self.frame, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        # Color picker
        self.color_button = tk.Button(self.frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.frame, text="Save as PNG", command=self.open_save_dialog)
        self.save_button.pack(side=tk.RIGHT, pady=10)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.last_x, self.last_y = None, None

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
        """Initialize the start point for drawing."""
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        """Draw on the canvas."""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.drawing_color, width=2)
            self.last_x, self.last_y = event.x, event.y

    def stop_draw(self, event):
        """Reset the last position."""
        self.last_x, self.last_y = None, None

    def use_pencil(self):
        """Set the tool to pencil."""
        self.drawing_color = self.color_button['text'] if self.color_button['text'] != "Choose Color" else "black"

    def use_eraser(self):
        """Set the tool to eraser."""
        self.drawing_color = self.bg

    def choose_color(self):
        """Choose the pencil color."""
        color = colorchooser.askcolor(color=self.drawing_color)
        if color[1]:
            self.drawing_color = color[1]
            self.color_button.config(text=color[1])

    def open_save_dialog(self):
        """Open a modal-like dialog window for saving options."""
        self.dialog = Toplevel(self.root)
        self.dialog.title("Save Options")
        
        dialog_width = 200
        dialog_height = 150
        center_x = int(self.root.winfo_x() + (self.root.winfo_width() / 2) - (dialog_width / 2))
        center_y = int(self.root.winfo_y() + (self.root.winfo_height() / 2) - (dialog_height / 2))

        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")
        self.dialog.resizable(False, False)

        self.color_option = IntVar(value=1)

        colorize_button = tk.Radiobutton(self.dialog, text="Colorized", variable=self.color_option, value=1)
        colorize_button.pack()

        grayscale_button = tk.Radiobutton(self.dialog, text="Grayscale", variable=self.color_option, value=0)
        grayscale_button.pack()

        save_button = tk.Button(self.dialog, text="Save", command=self.save_to_png)
        save_button.pack(pady=10)

    def save_to_png(self):
        """Save the current canvas to a PNG file with an option for colorized or grayscale."""
        self.dialog.destroy()

        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if not file_path:
            return

        ps_file = file_path + '.ps'

        colormode = 'color' if self.color_option.get() else 'gray'
        self.canvas.postscript(file=ps_file, colormode=colormode)

        try:
            image = Image.open(ps_file)
            image.load(scale=10)
            if not self.color_option.get():
                image = image.convert('L')
            image.save(file_path, 'PNG', quality=95)
        except Exception as e:
            messagebox.showerror("Error Saving Image", str(e))
        finally:
            import os
            os.remove(ps_file)
