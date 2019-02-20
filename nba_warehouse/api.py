import requests


class NBAApi:
    def __init__(self, url):
        self.url = url

    def get(self):
        response = requests.get(self.url)
        if response.ok:
            return response
        else:
            return None
