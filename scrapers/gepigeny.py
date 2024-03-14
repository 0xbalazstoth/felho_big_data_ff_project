import json
import random
import re
import time
from bs4 import BeautifulSoup
import requests

class GepigenyScraper:
    def __init__(self, base_url, save_callback):
        """
        Initializes the scraper.

        Parameters:
        - base_url: Entry widget for base url input.
        - save_callback: Function to call for saving the scraped data.
        """
        self.base_url = base_url
        self.save_callback = save_callback
    
    def scrape_gepigeny_comments(self):
        base_url = self.base_url.get()
        comments = []

        try:
            comm_req = requests.get(base_url)
            content = comm_req.content.decode("utf-8")
            soup = BeautifulSoup(content, 'lxml')
            last_page_regex = r"title='Oldal \d+ \/ (\d+)'"
            match = re.search(last_page_regex, content)
            last_page_number = int(match.group(1)) if match else 1
        except Exception as e:
            print(f"Error during initial request: {e}")
            return

        c_start = 0
        for page in range(1, last_page_number + 1):
            try:
                page_url = f"{base_url}&c_start={c_start}#comments" if page > 1 else base_url
                comm_req = requests.get(page_url)
                content = comm_req.content.decode("utf-8")
                soup = BeautifulSoup(content, 'lxml')

                page_comments = [div.get_text(strip=True) for div in soup.find_all('div', class_='comm_text')]
                comments.extend(page_comments)

                # Save or append comments to a JSON file after each page
                with open('gepigeny_comments.json', 'w', encoding='utf-8') as file:
                    json.dump(comments, file, ensure_ascii=False, indent=2)

                time.sleep(random.uniform(1, 5))
                c_start += 50
                print(f"Scraped comments from page {page}/{last_page_number}. Total comments so far: {len(comments)}")
            except Exception as e:
                print(f"Error scraping page {page} or saving comments: {e}")
                break

        print(f"Finished scraping. Total comments scraped: {len(comments)} across {last_page_number} pages.")
