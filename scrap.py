import requests
import cloudscraper
import json
import random
import time
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
    
    def save_html(self, url):
        response = self.scraper.get(url, proxies=self.proxies.get_bs4(), headers=self.agents.get_bs4())
        with open('novel.html', 'w', encoding='utf-8') as file:
            file.write(str(BeautifulSoup(response.content, 'html.parser')))
            
    def find_data(self, soup):
        title = soup.find('div', class_='seriestitlenu')
        description = soup.find('div', id='editdescription').find_all('p')
        type_ = soup.find('div', id='showtype').find('a').text
        region = soup.find('a', class_='genre lang').text
        genres = soup.find('div', id='seriesgenre').find_all('a')
        tags = soup.find('div', id='showtags').find_all('a')
        rating = soup.find('span', class_='uvotes').text
        release_year = soup.find('div', id='edityear').text
        cout_caps = soup.find('div', id='editstatus').text
        author = soup.find('div', id='showauthors').find('a').text
        
        completed = soup.find('div', id='showtranslated').text.strip()
        if completed == "Yes": completed = True
        else: completed = False
        
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
            "release_year": int(release_year.strip()),
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
                    
    
    def find_elements(self, soup: BeautifulSoup):
        pass

novels = Novel()
page = 2
soup = novels.get_soup("https://www.novelupdates.com/series/saturdays-master/")

# for i in range(1, 60):
#     soup_farm = novels.get_soup(f"https://www.novelupdates.com/series-ranking/?rank=sixmonths&pg={i}") 
#     novels.find_links(soup_farm)
#     time.sleep(random.uniform(1,3))
# print(len(novels.link_to_extract))
    
novels.find_elements(soup)