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

class PreprocessDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="Load dataset:").grid(row=0)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(master, textvariable=self.file_path_var, state='readonly')
        self.file_path_entry.grid(row=0, column=1)
        ttk.Button(master, text="Browse...", command=self.load_dataset).grid(row=0, column=2)

        # Checkboxes for preprocessing options
        self.clean_text_var = tk.BooleanVar()
        self.tokenization_var = tk.BooleanVar()
        self.lemmatization_var = tk.BooleanVar()

        ttk.Checkbutton(master, text="Clean Text", variable=self.clean_text_var).grid(row=1, columnspan=3, sticky='w')
        ttk.Checkbutton(master, text="Tokenization", variable=self.tokenization_var).grid(row=2, columnspan=3, sticky='w')
        ttk.Checkbutton(master, text="Lemmatization", variable=self.lemmatization_var).grid(row=3, columnspan=3, sticky='w')

        return master  # This line should return the dialog's body

    def load_dataset(self):
        file_types = [('CSV files', '*.csv'), ('JSON files', '*.json')]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.file_path_var.set(file_path)

    def apply(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a dataset.")
            return

        # Load dataset
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return

        # Apply selected preprocessing steps
        if self.clean_text_var.get():
            # Placeholder for text cleaning function
            pass
        if self.tokenization_var.get():
            # Placeholder for tokenization function
            pass
        if self.lemmatization_var.get():
            # Placeholder for lemmatization function
            pass

        messagebox.showinfo("Success", "Preprocessing completed.")