import customtkinter as ctk
from customtkinter import E, N, ON, S
from tkinter import ttk, simpledialog, messagebox, filedialog
import json
from scrapers.gepigeny import GepigenyScraper
from scrapers.markmyprofessor import MarkMyProfessorScraper
from scrapers.google_play import GooglePlayScraper

class ScrapeDialog(simpledialog.Dialog):

    def body(self, master):
        self.tab_control = ttk.Notebook(master)
        self.tab_google_play = ctk.CTkFrame(self.tab_control)
        self.tab_markmyprofessor = ctk.CTkFrame(self.tab_control)
        self.tab_gepigeny = ctk.CTkFrame(self.tab_control)
        self.tab_control.add(self.tab_google_play, text='Google Play')
        self.tab_control.add(self.tab_markmyprofessor, text='MarkMyProfessor')
        self.tab_control.add(self.tab_gepigeny, text='Gépigény')
        self.tab_control.pack(expand=1, fill='both')
        self.populate_google_play_tab(self.tab_google_play)
        self.populate_markmyprofessor_tab(self.tab_markmyprofessor)
        self.populate_gepigeny_tab(self.tab_gepigeny)
        return master

    def apply(self):
        pass

    def save_as_json(self, data):
        file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json'), ('All files', '*.*')])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, default=lambda x: None, ensure_ascii=False)
            messagebox.showinfo('Save', f'File has been saved as {file_path}')

    def save_txt_file(self, data):
        file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json'), ('All files', '*.*')])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            messagebox.showinfo('Save', f'File has been saved as {file_path}')

    def populate_google_play_tab(self, tab):
        label = ctk.CTkLabel(tab, text='Scrape reviews:')
        label.pack(pady=10)
        app_id_label = ctk.CTkLabel(tab, text='App ID:')
        app_id_label.pack(pady=(5, 0))
        self.app_id_entry = ctk.CTkEntry(tab)
        self.app_id_entry.pack(pady=(0, 10))
        scrape_button = ctk.CTkButton(tab, text='Get reviews', command=self.google_play_reviews)
        scrape_button.pack(pady=10)

    def populate_markmyprofessor_tab(self, tab):
        label = ctk.CTkLabel(tab, text='Search teacher(s):')
        label.pack(pady=10)
        self.name = ctk.CTkEntry(tab)
        self.name.pack(pady=(0, 10))
        name_search_button = ctk.CTkButton(tab, text='Get teachers', command=self.markmyprofessor_teachers)
        name_search_button.pack(pady=10)
        comm_label = ctk.CTkLabel(tab, text='Scrape comments')
        comm_label.pack(pady=10)
        scrape_comments_button = ctk.CTkButton(tab, text='Get comments', command=self.markmyprofessor_comments)
        scrape_comments_button.pack(pady=10)

    def populate_gepigeny_tab(self, tab):
        url_label = ctk.CTkLabel(tab, text='URL:')
        url_label.pack(pady=(5, 0))
        self.url = ctk.CTkEntry(tab)
        self.url.pack(pady=(0, 10))
        scrape_comments_button = ctk.CTkButton(tab, text='Get comments', command=self.scrape_gepigeny_comments)
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