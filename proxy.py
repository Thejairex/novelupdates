
from bs4 import BeautifulSoup

import random
import time
import requests
import json
import os


class Proxies:
    def __init__(self):
        if not os.path.exists("proxies.json"):
            print("no exite")
            response = requests.get("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=json")
            data = response.json()["proxies"]
            
            with open("proxies.json", 'w') as file:
                json.dump(data, file, indent=4)
            self.proxies = json.load(open("proxies.json"))
            del data, response
        else:
            self.proxies = json.load(open("proxies.json"))

    def get(self):
        proxy = random.choice(self.proxies)
        return {f"{proxy["protocol"]}": f"http://{proxy["proxy"]}",} 
    