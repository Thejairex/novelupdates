import requests
from bs4 import BeautifulSoup

from proxy import Proxies
from agent import Agent

proxies = Proxies()
agente = Agent()

def get_soup(url):
    response = requests.get(url, proxies=proxies.get_bs4(), headers=agente.get_bs4())
    return BeautifulSoup(response.content, 'html.parser')

soup = get_soup('https://novelupdates.com/')

print(soup.prettify())