import requests

from nba_warehouse.utils import HEADERS


class NBAApi:
    def __init__(self, url):
        self.url = url

    def get(self):
        response = requests.get(self.url, headers=HEADERS)
        if response.ok:
            return response
        else:
            return None
