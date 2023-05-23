import json
import logging
from typing import List

import requests


class Source:
    _coins = {}
    
    def __init__(self):
        coins_path = './src/sources/coins.json'
        self._coins = self.load_coins(coins_path)

    def get_coins(self):
        return self._coins

    def load_coins(self, coins_path: str) -> List[str]:
        with open(coins_path, 'r') as coins_file:
            coins = json.load(coins_file)
            coins_file.close()
            return coins

    def fetch(self, endpoint, headers = {}):
        try:
            return requests.get(endpoint, headers=headers)
        except requests.exceptions.RequestException as e:
            logging.error(f'Error making request to {endpoint}, exception={e}')