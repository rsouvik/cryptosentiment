import logging
from os import read
from sources.source import Source

import json
from datetime import datetime


class CryptoCompare(Source):
    crypto_compare_api_key = "90975105a7155b6940c614a67ea1e3ed6626ea7f033029bdae606e5cb3a863af"
    crypto_compare_endpoint = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit={:d}&e={}"

    last_mins_to_fetch = 60
    exchanges = ['CCCAGG', 'Coinbase']

    def __init__(self):
        super().__init__()

    def fetch_all(self):
        for coin in self.get_coins():
            for exchange in self.exchanges:
                logging.info(f'>>> Requesting {self.last_mins_to_fetch} for {coin} on {exchange}')
                yield from self.fetch_data(coin, exchange)

    def fetch_data(self, coin, exchange):
        crypto_compare_endpoint_url = self.crypto_compare_endpoint.format(coin, self.last_mins_to_fetch, exchange)
        raw_resp = self.fetch(crypto_compare_endpoint_url)
        response = raw_resp.json()
        logging.info(response)
        if response['Response'] == 'Success':
            for minute in response['Data']:
                yield {
                    'coin': coin,
                    'exchange': exchange,
                    'time': minute['time'],
                    'open': float(minute['open']),
                    'high': float(minute['high']),
                    'low': float(minute['low']),
                    'volumefrom': float(minute['volumefrom']),
                    'volumeto': float(minute['volumeto']),
                    'close': float(minute['close'])
                }
        
