import json
import os
import time
import yfinance as yf
#from influxdb import InfluxDBClient

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "hft"
org = "ddnusers"
token = "Y68gLteW69vpkdz3f15BFnvK6cVcAvwpUSx-e5kG8S3izH5DDSGDbd39zIneFuBUcumPeaXRUCMF3KG3Q7wh4w=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

class HFTDash:
    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )

    def run(self):
        while True:
            with open('data/data.json') as data_file:
                data = json.load(data_file)
                for share in data['shares']:
                    ticker = yf.Ticker(share['symbol'])
                    history = ticker.history()
                    last_quote = (history.tail(1)['Close'].iloc[0])
                    json_body = [
                        {
                            "measurement": "price",
                            "tags": {
                                "name": share['name']
                            },
                            "fields": {
                                "amount": float(last_quote)
                            }
                        },
                        {
                            "measurement": "estate",
                            "tags": {
                                "name": share['name'],
                            },
                            "fields": {
                                "quantity": float(share['estate']['quantity']),
                                "received_dividend":
                                    float(share['estate']['received_dividend']),
                            }
                        },
                        {
                            "measurement": "purchase",
                            "tags": {
                                "name": share['name'],
                            },
                            "fields": {
                                "quantity": float(share['purchase']['quantity']),
                                "cost_price":
                                    float(share['purchase']['cost_price']),
                                "fee": float(share['purchase']['fee'])
                            }
                        }
                    ]
                    write_api = self.client.write_api(write_options=SYNCHRONOUS)
                    write_api.write(bucket, org, json_body)
                    time.sleep(60)


if __name__ == "__main__":
    hftd = HFTDash()
    hftd.run()