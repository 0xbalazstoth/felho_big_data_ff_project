import json
import os
from tkinter import filedialog
import requests
import urllib.parse

class MarkMyProfessorScraper:
    def __init__(self, name_entry, save_callback):
        """
        Initializes the scraper.

        Parameters:
        - name_entry: Entry widget for teacher name input.
        - save_callback: Function to call for saving the scraped data.
        """
        self.name_entry = name_entry
        self.save_callback = save_callback
    
    def search_teachers(self):
        name_query = self.name_entry.get()
        name_url = f"https://backend.markmyprofessor.com/api/search?search={urllib.parse.quote(name_query)}&locale=hu"
        teachers_req = requests.get(name_url)
        teachers_content = teachers_req.content.decode('utf8')
        
        teachers_json = json.loads(teachers_content)
        
        self.save_callback(teachers_json)
        
    def scrape_markmyprofessor_comments(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                teachers_data = data["data"]
                teachers = teachers_data["teachers"]
                for teacher in teachers:
                    if teacher["rating_results_avg_rating"] is not None:
                        all_comments = []
                        curr_page = 1
                        slug = teacher["slug"]
                        last_page = self.get_markmyprofessor_teacher_get_last_page(slug)
                        while curr_page <= last_page:
                            comments = self.scrape_markmyprofessor_comment(slug, curr_page)
                            all_comments.extend(comments)
                            curr_page += 1
            
    def get_markmyprofessor_teacher_get_last_page(self, slug):
        url = f"https://backend.markmyprofessor.com/api/teacher-profiles/{slug}/ratings?page=1&locale=hu"
        req = requests.get(url)
        json_data = json.loads(req.content)
        return json_data['data']['ratings']['meta']['last_page']
                        
    def scrape_markmyprofessor_comment(self, slug, page):
        url = f"https://backend.markmyprofessor.com/api/teacher-profiles/{slug}/ratings?page={page}&locale=hu"
        req = requests.get(url)
        with open(f'./{slug}_comments_{page}.json', 'w', encoding='utf-8') as comments_file:
                            json.dump(json.loads(req.content), comments_file, ensure_ascii=False, indent=4)
        return json.loads(req.content)