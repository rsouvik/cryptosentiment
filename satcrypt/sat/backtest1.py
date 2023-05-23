import numpy as np

from backtesting.test import GOOG
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
import pandas as pd

import yfinance as yf
import matplotlib.dates as md
from datetime import datetime as dt

import matplotlib.pyplot as plt

from sat.backtest import backtest_m, nb_calc_sentiment_score_a, nb_causal_rolling_average
from sat.fetch_sentiment_for_range import fetch, fetchBTC


# df = yf.download(tickers='BTC-USD', start=sd, end=ed, interval="1m")
# df = yf.download(tickers='BTC-USD', start=sd, end=ed)

# Sentiment
df = fetch("select * from tempsentiment WHERE creationtime >= '2022-05-27 13:45:00'")
# df = yf.download(tickers='BTC-USD', start=sd, end=ed, interval="1d")

# BTC price
# df.to_csv('volume_btc_july.csv')

df1 = fetchBTC("select * from tempbtc WHERE creationtime >= '2022-05-27 13:45:00'")
# df1 = yf.download(tickers='BTC-USD', start=sd, end=ed, interval="1m")

# initialise some labels for the plot
# datenum_sent_data = [md.date2num(dt.fromtimestamp(el)) for el in df["time"]]
# datenum_price_data = [md.date2num(dt.fromtimestamp(el)) for el in df1["time"]]

# set up the figure
fig, ax = plt.subplots(4, 1, sharex=True, sharey=False)

datenum_sent_data = df["creationtime"]
datenum_price_data = df["creationtime"]

# define the window size for the sentiment score calculation
# vary window size
n_days = 7
window_size = 24 * n_days
window_size = 3

sent_ratio_smooth = nb_causal_rolling_average(df["Volume"].astype(float), window_size)

# generate the sentiment score
sent_score = nb_calc_sentiment_score_a(df["Volume"].astype(float), window_size, window_size)

# print(sent_score)

bt = backtest_m(df1["Volume"], sent_score, 1, 0)

stats = bt.shape
print(stats)

# plot stuff
ax[0].grid(linewidth=0.4)
ax[1].grid(linewidth=0.4)
ax[2].grid(linewidth=0.4)
ax[3].grid(linewidth=0.4)
ax[0].plot(datenum_price_data, df1["Volume"], linewidth=0.5)
ax[1].plot(datenum_sent_data, sent_score, linewidth=0.5)
ax[2].plot(datenum_price_data, bt, linewidth=0.5)
ax[3].plot(datenum_sent_data, sent_ratio_smooth, linewidth=0.5)

# label axes
ax[0].set_ylabel("Price")
ax[1].set_ylabel("Sentiment score")
ax[2].set_ylabel("PnL")
ax[3].set_ylabel("Rolling average sent score")
ax[1].set_ylim([-5.5, 5.5])

# generate the time axes
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )
ax[0]=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
ax[0].xaxis.set_major_formatter(xfmt)

# show the plot
plt.show()

