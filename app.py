import random
import re
import time
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from google_play_scraper import Sort, reviews, reviews_all, search
import os
import json
import urllib.parse
import requests
import html
from bs4 import BeautifulSoup

from scrapers.gepigeny import GepigenyScraper
from scrapers.markmyprofessor import MarkMyProfessorScraper
from scrapers.google_play import GooglePlayScraper

class ScrapeDialog(simpledialog.Dialog):
    def body(self, master):
        # Create the tab control (Notebook)
        self.tab_control = ttk.Notebook(master)

        # Create tabs
        self.tab_google_play = ttk.Frame(self.tab_control)
        self.tab_markmyprofessor = ttk.Frame(self.tab_control)
        self.tab_gepigeny = ttk.Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.tab_google_play, text='Google Play')
        self.tab_control.add(self.tab_markmyprofessor, text='MarkMyProfessor')
        self.tab_control.add(self.tab_gepigeny, text='Gépigény')

        # Pack the Notebook
        self.tab_control.pack(expand=1, fill="both")

        # Populate the tabs with content
        self.populate_google_play_tab(self.tab_google_play)
        self.populate_markmyprofessor_tab(self.tab_markmyprofessor)
        self.populate_gepigeny_tab(self.tab_gepigeny)

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
            
    def save_txt_file(self, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            messagebox.showinfo("Save", f"File has been saved as {file_path}")

    def populate_google_play_tab(self, tab):
        label = ttk.Label(tab, text="Scrape reviews:")
        label.pack(pady=10)
        
        app_id_label = ttk.Label(tab, text="App ID:")
        app_id_label.pack(pady=(5, 0))
        self.app_id_entry = ttk.Entry(tab)
        self.app_id_entry.pack(pady=(0, 10))
        
        scrape_button = ttk.Button(tab, text="Get reviews", command=self.google_play_reviews)
        scrape_button.pack(pady=10)

    def populate_markmyprofessor_tab(self, tab):
        label = ttk.Label(tab, text="Search teacher(s):")
        label.pack(pady=10)
        self.name = ttk.Entry(tab)
        self.name.pack(pady=(0, 10))
        
        name_search_button = ttk.Button(tab, text="Get teachers", command=self.markmyprofessor_teachers)
        name_search_button.pack(pady=10)
        
        comm_label = ttk.Label(tab, text="Scrape comments")
        comm_label.pack(pady=10)
        
        scrape_comments_button = ttk.Button(tab, text="Get comments", command=self.markmyprofessor_comments)
        scrape_comments_button.pack(pady=10)
        
    def populate_gepigeny_tab(self, tab):
        url_label = ttk.Label(tab, text="URL:")
        url_label.pack(pady=(5, 0))
        self.url = ttk.Entry(tab)
        self.url.pack(pady=(0, 10))
        
        scrape_comments_button = ttk.Button(tab, text="Get comments", command=self.scrape_gepigeny_comments)
        scrape_comments_button.pack(pady=10)
        
    def scrape_gepigeny_comments(self):
        gepigeny_scraper = GepigenyScraper(self.url, self.save_as_json)
        gepigeny_scraper.scrape_gepigeny_comments()

    def google_play_reviews(self):
        google_play_scraper = GooglePlayScraper(self.app_id_entry, self.save_as_json)
        google_play_scraper.scrape_reviews()
        
    def markmyprofessor_teachers(self):
        markmyprofessor_scraper = MarkMyProfessorScraper(self.name, self.save_as_json)
        markmyprofessor_scraper.search_teachers()
        
    def markmyprofessor_comments(self):
        markmyprofessor_scraper = MarkMyProfessorScraper(self.name, self.save_as_json)
        markmyprofessor_scraper.scrape_markmyprofessor_comments()
        
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
