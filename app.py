import random
import re
import time
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from google_play_scraper import Sort, reviews, reviews_all, search
import os
import json
import urllib.parse
import pandas as pd
import requests
import html
from bs4 import BeautifulSoup

from dialogs.preprocess_dialog import PreprocessDialog
from dialogs.scraper_dialog import ScrapeDialog
from scrapers.gepigeny import GepigenyScraper
from scrapers.markmyprofessor import MarkMyProfessorScraper
from scrapers.google_play import GooglePlayScraper

def open_scrape_dialog():
    dialog = ScrapeDialog(root, "Scrape Options")

def open_preprocess_dialog():
    dialog = PreprocessDialog(root, "Preprocess Options")

root = tk.Tk()
root.title("Scrape Application")

# Desired window width and height
window_width = 400
window_height = 200

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

preprocess_button = tk.Button(root, text="Preprocess", command=open_preprocess_dialog)
preprocess_button.pack(pady=2)

root.mainloop()
