import requests
import cloudscraper
from bs4 import BeautifulSoup

from proxy import Proxies
from agent import Agent

proxies = Proxies()
agente = Agent()
scraper = cloudscraper.create_scraper()

def get_soup(url):
    response = scraper.get(url, proxies=proxies.get_bs4(), headers=agente.get_bs4())
    return BeautifulSoup(response.content, 'html.parser')

soup = get_soup('https://novelupdates.com/')

for i in soup.find_all('a'):
    print(i.get('href'))
    
base = 'https://novelupdates.com/'
with open('novelupdates.txt', 'w', encoding='utf-8') as file:
    for link in soup.find_all('a'):
        if str(link.get("href")).startswith(base):
            file.write(str(i.get('href')) + '\n')