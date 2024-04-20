import customtkinter as ctk
from customtkinter import S
import tkinter as tk
from dialogs.preprocess_dialog import PreprocessDialog
from dialogs.scraper_dialog import ScrapeDialog

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
scrape_button = ctk.CTkButton(root, text='Scrape', command=open_scrape_dialog)
scrape_button.pack(pady=40)
preprocess_button = ctk.CTkButton(root, text='Preprocess', command=open_preprocess_dialog)
preprocess_button.pack(pady=2)
root.mainloop()