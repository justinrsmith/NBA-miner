import requests


class NBAApi:
    def __init__(self, url):
        self.url = url
        self.response = None

    def get(self):
        self.response = requests.get(self.url)
        if self.response.ok:
            return self.response
        else:
            return None
