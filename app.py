import customtkinter as ctk
from customtkinter import S
import tkinter as tk
from dialogs.preprocess_dialog import PreprocessDialog
from dialogs.scraper_dialog import ScrapeDialog
from PIL import Image, ImageTk

def open_scrape_dialog():
    dialog = ScrapeDialog(root, 'Scrape Options')

def open_preprocess_dialog():
    dialog = PreprocessDialog(root, 'Preprocess Options')

root = ctk.CTk()
root.title('Scrape Application')
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Create a frame to contain the buttons
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(expand=True)

scrape_img = ImageTk.PhotoImage(Image.open("assets/scrape.png").resize((18, 18), Image.ANTIALIAS))
scrape_button = ctk.CTkButton(button_frame, text='Scrape', command=open_scrape_dialog, image=scrape_img, compound="left", text_color="#000", fg_color="#F9F9F9", hover_color="#D0D0D0")
scrape_button.pack(pady=4)

preprocess_img = ImageTk.PhotoImage(Image.open("assets/process.png").resize((18, 18), Image.ANTIALIAS))
preprocess_button = ctk.CTkButton(button_frame, text='Preprocess', command=open_preprocess_dialog, image=preprocess_img, compound="left", text_color="#000", fg_color="#F9F9F9", hover_color="#D0D0D0")
preprocess_button.pack(pady=4)

button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
