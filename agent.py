from fake_useragent import UserAgent

class Agent:
    def __init__(self):
        self.useragent = UserAgent()

    def get(self):
        return self.useragent.random
    
    def change(self):
        self.useragent = UserAgent()
        
