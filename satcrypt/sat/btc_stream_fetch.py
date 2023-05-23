import yfinance as yf
from datetime import date
from datetime import timedelta

# sd = datetime(2022, 3, 17)
from sat.tweetsetl import dbConnectCrypto
from sat.utils import datetime_from_utc_to_local

sd = date.today() - timedelta(days=1)
# ed = datetime(2022, 3, 18)
ed = date.today()
td = date.today() + timedelta(days=1)

df = yf.download(tickers='BTC-USD', start=ed, end=td, interval="1m")
# df = yf.download(tickers='ETH-USD', start=ed, end=td, interval="1m")

df['datet'] = df.index
for index, df1 in df.iterrows():
    # creation_time = datetime_from_utc_to_local(df1['datet'])
    # print(creation_time)
    # dbConnectCrypto(creation_time, df1['Open'], df1['High'], df1['Low'], df1['Close'], df1['Adj Close'], df1['Volume'])
    dbConnectCrypto(df1['datet'], df1['Open'], df1['High'], df1['Low'], df1['Close'], df1['Adj Close'], df1['Volume'])

print(df)
