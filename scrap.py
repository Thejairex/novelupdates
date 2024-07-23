import cloudscraper
import random
import time
import os
import pandas as pd
from bs4 import BeautifulSoup

from proxy import Proxies
from agent import Agent

    
class Novel:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.proxies = Proxies() 
        self.agents = Agent()
        self.link_to_extract = set()
        self.link_extracted = set()
        
    def get_soup(self, url):
        response = self.scraper.get(url, proxies=self.proxies.get_bs4(), headers=self.agents.get_bs4())
        return BeautifulSoup(response.content, 'html.parser')
    
            
    def find_data(self, soup):
        # try:
        title = soup.find('div', class_='seriestitlenu')
        description = soup.find('div', id='editdescription').find_all('p')
        type_ = soup.find('div', id='showtype').find('a').text
        region = soup.find('a', class_='genre lang').text
        genres = soup.find('div', id='seriesgenre').find_all('a')
        tags = soup.find('div', id='showtags').find_all('a')
        rating = soup.find('span', class_='uvotes').text
        if soup.find('div', id='edityear').text:
            release_year = soup.find('div', id='edityear').text
            release_year = int(release_year.strip())
        else: release_year = 0000
        
        cout_caps = soup.find('div', id='editstatus').text
        author = soup.find('div', id='showauthors').find('a').text
        
        completed = soup.find('div', id='showtranslated').text.strip()
        if completed == "Yes": completed = True
        else: completed = False
        
        #get recommendations (6 links)
        recommendations = soup.find_all('h5', class_="seriesother")[-2].find_all_next('a', limit = 6)
        recommendations = [recom.get('href') for recom in recommendations if recom.get('href').startswith("https://www.novelupdates.com/series/")]
        for recom in recommendations: 
            if recom not in self.link_to_extract: self.link_to_extract.add(recom)
        
        return {
            "title": title.text,
            "description": " ".join([des.text for des in description]),
            "type": type_,
            "region": region.replace("(", "").replace(")", ""),
            "genres": [genre.text for genre in genres],
            "tags": [tag.text for tag in tags],
            "rating": float(rating.split()[0].replace("(", "")),
            "release_year": release_year,
            "captions": int(cout_caps.strip().split(" ")[0]),
            "completed": completed,
            "author": author
        }

    def find_links(self, soup: BeautifulSoup):
        body = soup.find('div', class_="w-blog-content other").find_all('a')

        for link in body:
            url = link.get('href')
            if url:
                if url.startswith("https://www.novelupdates.com/series/"):
                    self.link_to_extract.add(url)

    
    def create_dataset(self):
        data = []
        try:
            print("Start scraping...")
            for link in self.link_to_extract:
                if link in self.link_extracted: continue
                
                soup = self.get_soup(link)
                data.append(self.find_data(soup))
                time.sleep(random.uniform(1,3))
                self.link_extracted.add(link)
                # self.link_to_extract.remove(link)
            return data
        except KeyboardInterrupt:
            print(link)
            return data
        
        except Exception as e:
            raise e
    
    def export_links(self):
        with open('novel_links.txt', 'w') as file:
            for link in self.link_to_extract:
                file.write(link + '\n')
            file.close()
    
    def import_links(self):
        with open('novel_links.txt', 'r') as file:
            for line in file:
                line = line.strip()
                self.link_to_extract.add(line)
            file.close()

if __name__ == "__main__":
    novels = Novel()
    page = 1
    
    if not os.path.exists('novel_links.txt'):
        try: 
            while page <= 892:
                soup_farm = novels.get_soup(f"https://www.novelupdates.com/series-ranking/?rank=sixmonths&pg={page}") 
                novels.find_links(soup_farm)
                time.sleep(random.uniform(1,3))
                print(len(novels.link_to_extract))
                page += 1
            
            # export set
            novels.export_links()

        except KeyboardInterrupt:
            # export current set
            novels.export_links()
            
        except Exception as e:
            raise e
    else:
        novels.import_links()

    print(f"Total novels: {len(novels.link_to_extract)}")
    
    
    data = novels.create_dataset()
    print(data)
