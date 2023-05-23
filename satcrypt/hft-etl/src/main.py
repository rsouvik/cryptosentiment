import logging
from time import sleep

from config.influxdb.influxdb import InfluxDbConfig

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS  # async or batch more appropriate in context?
from sources.cryptocompare import CryptoCompare


class Collect:
    def __init__(self):
        self.influxdbconfig = InfluxDbConfig()
        self.influx_client = InfluxDBClient(url=self.influxdbconfig.url, token=self.influxdbconfig.token, org=self.influxdbconfig.org)
        self.influx_write = self.influx_client.write_api(write_options=SYNCHRONOUS)

    def run_collection(self):
        self.collect_cryptocompare()

        self.influx_client.close()

    def collect_cryptocompare(self):
        logging.info(">>> Running collection for CryptoCompare...")
        crypto_compare = CryptoCompare()
        for data_point in crypto_compare.fetch_all():
            timestamp_nanos = int(data_point["time"] * 1e9)
            record = (
                Point("crypto")
                .tag('coin', data_point['coin'])
                .tag('exchange', data_point['exchange'])
                .time(timestamp_nanos)
                .field("open", data_point["open"])
                .field("high", data_point["high"])
                .field("low", data_point["low"])
                .field("volumefrom", data_point["volumefrom"])
                .field("volumeto", data_point["volumeto"])
                .field("close", data_point["close"])
            )
            self.influx_write.write(bucket=self.influxdbconfig.bucket, org=self.influxdbconfig.org, record=record)


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

interval = 3600  # one hour in seconds
while True:
    logging.info("Starting collection...")
    collect = Collect()
    collect.run_collection()
    logging.info("Collection finished...")
    sleep(interval)