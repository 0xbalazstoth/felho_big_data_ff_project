import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from google_play_scraper import Sort, reviews, reviews_all, search

class GooglePlayScraper:
    def __init__(self, app_id_entry, save_callback):
        """
        Initializes the scraper with necessary UI components and callbacks.

        Parameters:
        - app_id_entry: Entry widget for app ID input.
        - save_callback: Function to call for saving the scraped data.
        """
        self.app_id_entry = app_id_entry
        self.save_callback = save_callback

    def scrape_reviews(self):
        """
        Scrapes reviews for the app ID specified in the app_id_entry widget,
        then saves the data using the save_callback function.
        """
        app_id = self.app_id_entry.get()
        print(app_id)
        try:
            app_reviews = reviews_all(
                app_id=app_id,
                lang='hu',
                country='hu',
                sleep_milliseconds=100
            )
            self.save_callback(app_reviews)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape Google Play reviews: {e}")
