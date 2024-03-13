import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from google_play_scraper import Sort, reviews, reviews_all
import os
import json

class ScrapeDialog(simpledialog.Dialog):
    def body(self, master):
        # Create the tab control (Notebook)
        self.tab_control = ttk.Notebook(master)

        # Create tabs
        self.tab_google_play = ttk.Frame(self.tab_control)
        self.tab_twitter = ttk.Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.tab_google_play, text='Google Play')
        self.tab_control.add(self.tab_twitter, text='Twitter')

        # Pack the Notebook
        self.tab_control.pack(expand=1, fill="both")

        # Populate the tabs with content
        self.populate_google_play_tab(self.tab_google_play)
        self.populate_twitter_tab(self.tab_twitter)

        return master

    def apply(self):
        pass  # This function can be used to perform actions when the dialog is submitted.

    def save_as_json(self, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:  # only save if the user didn't cancel the dialog
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, default=lambda x: None, ensure_ascii=False)
            messagebox.showinfo("Save", f"File has been saved as {file_path}")

    def populate_google_play_tab(self, tab):
        label = ttk.Label(tab, text="Google Play Tab Content")
        label.pack(pady=10)
        
        app_id_label = ttk.Label(tab, text="App ID:")
        app_id_label.pack(pady=(5, 0))
        self.app_id_entry = ttk.Entry(tab)
        self.app_id_entry.pack(pady=(0, 10))
        
        scrape_button = ttk.Button(tab, text="Scrape Google Play", command=self.scrape_google_play)
        scrape_button.pack(pady=10)

    def populate_twitter_tab(self, tab):
        label = ttk.Label(tab, text="Twitter Tab Content")
        label.pack(pady=10)
        
        scrape_button = ttk.Button(tab, text="Scrape Twitter", command=self.scrape_twitter)
        scrape_button.pack(pady=10)

    def scrape_google_play(self):
        print("Scraping Google Play...")
        app_id = self.app_id_entry.get()
        app_reviews = reviews_all(
            app_id=app_id,
            lang='hu',
            country='hu',
            sleep_milliseconds=20
        )

        self.save_as_json(app_reviews)
        
    def scrape_twitter(self):
        print("Scraping Twitter...")
        messagebox.showinfo("Scraping", "Scraping Twitter. Check the console for updates.")

def open_scrape_dialog():
    dialog = ScrapeDialog(root, "Scrape Options")

root = tk.Tk()
root.title("Scrape Application")

# Desired window width and height
window_width = 800
window_height = 600

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position to center the window
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# Set the window's geometry
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

scrape_button = tk.Button(root, text="Scrape", command=open_scrape_dialog)
scrape_button.pack(pady=40)

root.mainloop()
