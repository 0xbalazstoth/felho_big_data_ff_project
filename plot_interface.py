import tkinter as tk
from tkinter import LabelFrame, filedialog, messagebox, Toplevel, IntVar, colorchooser, Scale, Menubutton, Menu
from PIL import Image

class PlotInterface:
    def __init__(self, width=800, height=600, bg="white", title="OEplotter", min_width=800, min_height=800):
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

        self.drawing_color = "black"
        self.current_tool = "pencil"

        self.pencil_button = tk.Button(self.frame, text="Pencil", command=self.use_pencil)
        self.pencil_button.pack(side=tk.LEFT)
        self.color_button = tk.Button(self.frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(self.frame, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.frame, text="Save as PNG", command=self.open_save_dialog)
        self.save_button.pack(side=tk.RIGHT, pady=10)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        self.hand_drawn_elements = []
        self.eraser_indicator = None
        
        self.settings_button = tk.Button(self.frame, text="Settings", command=self.open_settings_dialog)
        self.settings_button.pack(side=tk.LEFT)
        
        self.clear_button = tk.Button(self.frame, text="Clear Drawing", command=self.clear_hand_drawing)
        self.clear_button.pack(side=tk.LEFT)
        
        self.pencil_size = IntVar(value=2)
        self.eraser_size = IntVar(value=10)

        self.pencil_size_slider = Scale(self.frame, from_=1, to=10, orient=tk.HORIZONTAL, label="Pencil Size", variable=self.pencil_size)
        self.eraser_size_slider = Scale(self.frame, from_=1, to=50, orient=tk.HORIZONTAL, label="Eraser Size", variable=self.eraser_size)

        self.zoom_scale = 1.0  # Initialize zoom scale to 1:1

        # Add zoom in and zoom out buttons
        self.zoom_in_button = tk.Button(self.frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT)

        self.zoom_out_button = tk.Button(self.frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT)
        
        self.is_panning = False  # Track whether panning is active
        self.pan_start_x = None
        self.pan_start_y = None

        # Bind mouse events for panning
        self.canvas.bind("<Button-2>", self.start_pan)  # Middle mouse button to start panning
        self.canvas.bind("<B2-Motion>", self.pan)       # Middle mouse button drag to pan
        self.canvas.bind("<ButtonRelease-2>", self.end_pan)

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
        
    def start_pan(self, event):
        """Start panning action."""
        self.canvas.scan_mark(event.x, event.y)
        self.is_panning = True
        self.pan_start_x, self.pan_start_y = event.x, event.y

    def pan(self, event):
        """Handle panning as the mouse moves."""
        if self.is_panning:
            # Calculate the distance moved from the start point
            dx, dy = event.x - self.pan_start_x, event.y - self.pan_start_y
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            self.pan_start_x, self.pan_start_y = event.x, event.y

    def end_pan(self, event):
        """End the panning action."""
        self.is_panning = False
        self.pan_start_x = None
        self.pan_start_y = None
        
    def zoom_in(self):
        """Zoom into the canvas."""
        zoom_factor = 1.1
        self.apply_zoom(zoom_factor)

    def zoom_out(self):
        """Zoom out of the canvas."""
        # Decrease the zoom scale by 10% from 1 (not cumulative)
        zoom_factor = 0.9
        self.apply_zoom(zoom_factor)

    def apply_zoom(self, zoom_factor):
        """Apply the given zoom factor to the canvas."""
        # Use the center of the canvas for the zoom origin
        x_origin = self.canvas.winfo_width() / 2
        y_origin = self.canvas.winfo_height() / 2
        self.canvas.scale("all", x_origin, y_origin, zoom_factor, zoom_factor)

        # Reset the scroll region to encompass the new canvas size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def clear_hand_drawing(self):
        """Clear only the hand-drawn elements from the canvas."""
        for element in self.hand_drawn_elements:
            self.canvas.delete(element)
        self.hand_drawn_elements.clear()
        
    def open_settings_dialog(self):
        """Open a settings dialog with options for drawing settings."""
        self.settings_dialog = Toplevel(self.root)
        self.settings_dialog.title("Settings")
        
        # Set geometry and make the dialog modal-like
        dialog_width, dialog_height = 300, 250
        center_x = self.root.winfo_x() + (self.root.winfo_width() / 2) - (dialog_width / 2)
        center_y = self.root.winfo_y() + (self.root.winfo_height() / 2) - (dialog_height / 2)
        self.settings_dialog.geometry(f"{dialog_width}x{dialog_height}+{int(center_x)}+{int(center_y)}")
        self.settings_dialog.resizable(False, False)

        # Drawing settings section
        drawing_frame = LabelFrame(self.settings_dialog, text="Drawing Settings", padx=10, pady=10)
        drawing_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Pencil size setting
        pencil_size_frame = LabelFrame(drawing_frame, text="Pencil Size", padx=10, pady=10)
        pencil_size_frame.pack(padx=5, pady=5, fill="both", expand=True)
        tk.Scale(pencil_size_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.pencil_size).pack(fill="x", expand=True)

        # Eraser size setting
        eraser_size_frame = LabelFrame(drawing_frame, text="Eraser Size", padx=10, pady=10)
        eraser_size_frame.pack(padx=5, pady=5, fill="both", expand=True)
        tk.Scale(eraser_size_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.eraser_size).pack(fill="x", expand=True)

    def start_draw(self, event):
        """Initialize the start point for drawing."""
        self.last_x, self.last_y = event.x, event.y
        if self.current_tool == "eraser":
            self.create_eraser_indicator(event.x, event.y)

    def draw(self, event):
        """Draw on the canvas based on the current tool and its size."""
        if self.last_x and self.last_y:
            if self.current_tool == "pencil":
                line_id = self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    fill=self.drawing_color, width=self.pencil_size_slider.get(),
                    capstyle=tk.ROUND, smooth=tk.TRUE)
                self.hand_drawn_elements.append(line_id)
            elif self.current_tool == "eraser":
                overlapping_items = self.canvas.find_overlapping(
                    event.x - self.eraser_size_slider.get()/2,
                    event.y - self.eraser_size_slider.get()/2,
                    event.x + self.eraser_size_slider.get()/2,
                    event.y + self.eraser_size_slider.get()/2)
                for item in overlapping_items:
                    if item in self.hand_drawn_elements:
                        self.canvas.delete(item)
                        self.hand_drawn_elements.remove(item)
                self.move_eraser_indicator(event.x, event.y)
        self.last_x, self.last_y = event.x, event.y

    def stop_draw(self, event):
        """Reset the last position and remove the eraser indicator."""
        self.last_x, self.last_y = None, None
        if self.current_tool == "eraser":
            self.remove_eraser_indicator() 

    def use_pencil(self):
        """Set the tool to pencil."""
        self.current_tool = "pencil"
        self.hide_eraser_indicator()

    def use_eraser(self):
        """Set the tool to eraser."""
        self.current_tool = "eraser"
        self.show_eraser_indicator()
        
    def show_eraser_indicator(self):
        """Show the eraser indicator on the canvas."""
        if not self.eraser_indicator:
            # Create an oval that follows the mouse
            self.eraser_indicator = self.canvas.create_oval(0, 0, 0, 0, outline="gray", width=2)
        self.update_eraser_indicator(self.root.winfo_pointerx() - self.root.winfo_rootx(),
                                     self.root.winfo_pointery() - self.root.winfo_rooty())
        
    def hide_eraser_indicator(self):
        """Hide the eraser indicator."""
        if self.eraser_indicator:
            self.canvas.delete(self.eraser_indicator)
            self.eraser_indicator = None

    def update_eraser_indicator(self, x, y):
        """Update the position of the eraser indicator to follow the mouse."""
        if self.eraser_indicator:
            radius = self.eraser_size_slider.get() / 2
            self.canvas.coords(self.eraser_indicator, x - radius, y - radius, x + radius, y + radius)
            
    def create_eraser_indicator(self, x, y):
        """Create an eraser indicator that follows the cursor."""
        radius = self.eraser_size_slider.get() / 2
        self.eraser_indicator = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            outline="gray", width=1, dash=(4, 2))

    def move_eraser_indicator(self, x, y):
        """Move the eraser indicator with the cursor."""
        if self.eraser_indicator:
            radius = self.eraser_size_slider.get() / 2
            self.canvas.coords(
                self.eraser_indicator,
                x - radius, y - radius, x + radius, y + radius)

    def remove_eraser_indicator(self):
        """Remove the eraser indicator from the canvas."""
        if self.eraser_indicator:
            self.canvas.delete(self.eraser_indicator)
            self.eraser_indicator = None

    def choose_color(self):
        """Open a color chooser dialog and set the pencil color."""
        color = colorchooser.askcolor(color=self.drawing_color)
        if color[1]:
            self.drawing_color = color[1]

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
