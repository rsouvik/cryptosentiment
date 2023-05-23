from backtesting.test import GOOG
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
import pandas as pd

import yfinance as yf
from datetime import datetime

from sat.fetch_sentiment_for_range import fetch, fetchBTC

sd = datetime(2022, 5, 2)
ed = datetime(2022, 5, 3)

# df = yf.download(tickers='BTC-USD', start=sd, end=ed, interval="1m")
# df = yf.download(tickers='BTC-USD', start=sd, end=ed)

# Sentiment
df = fetch("select * from tempsentiment")
# df = yf.download(tickers='BTC-USD', start=sd, end=ed, interval="1d")

# BTC price
# df.to_csv('volume_btc_july.csv')

df1 = fetchBTC("select * from tempbtc")
# df1 = yf.download(tickers='BTC-USD', start=sd, end=ed, interval="1m")


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).shift(periods=-30).rolling(n).mean()
    # return pd.Series(values).shift(periods=-20).ewm(span=n, adjust=False).mean()
    # return pd.Series(values).ewm(span=n, adjust=False).mean()


"""
Strategy: If N=10 moving av of metric is higher than N=20, buy (long)
"""


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 5  # 10
    n2 = 10

    def init(self):
        # Precompute the two moving averages
        # self.sma1 = self.I(SMA, self.data.Close, self.n1)
        # self.sma2 = self.I(SMA, self.data.Close, self.n2)

         self.sma1 = self.I(SMA, df.Volume, self.n1)
         self.sma2 = self.I(SMA, df.Volume, self.n2)

    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()


# bt = Backtest(GOOG, SmaCross, cash=10_000, commission=.002)
bt = Backtest(df1, SmaCross, cash=20000000, commission=.002)

stats = bt.run()
print(stats)

bt.plot()
