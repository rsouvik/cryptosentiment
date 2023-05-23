# Create
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from sat.dbconnect import DbConnect, DbConnectExec
from sat.load_df_to_db import postgresql
from sat.preprocess_tweets import preprocess
from sat.tweet_sentiment import sentiment

query = "TRUNCATE TABLE tempbtc;"

data_count = DbConnectExec(query)
print(data_count)

runquery = "INSERT INTO tempbtc (creationtime,open,high,low,volume,close) " \
           "WITH cte_bullish AS " \
           "(SELECT round_time_5m(\"Creationtime\") hour_beginning, COUNT(\"Sentiment\") bullish_count " \
            "FROM \"twittertweetsentimentn\" " \
           "WHERE \"Creationtime\" IS NOT NULL AND \"Sentiment\" = 1 " \
           "GROUP BY round_time_5m(\"Creationtime\") " \
           "ORDER BY round_time_5m(\"Creationtime\") ASC), " \
           "cte_bearish AS ( " \
           "SELECT round_time_5m(\"Creationtime\") hour_beginning, COUNT(\"Sentiment\") bearish_count " \
           "FROM \"twittertweetsentimentn\" " \
           "WHERE \"Creationtime\" IS NOT NULL " \
           "AND \"Sentiment\" = -1 " \
           "GROUP BY round_time_5m(\"Creationtime\") " \
           "ORDER BY round_time_5m(\"Creationtime\") ASC), " \
           "cte_ratio AS ( " \
           "SELECT cte_bearish.hour_beginning tm, round(cte_bullish.bullish_count / cte_bearish.bearish_count::numeric, 2) AS ratio " \
           "FROM cte_bearish INNER JOIN cte_bullish ON cte_bullish.hour_beginning = cte_bearish.hour_beginning), " \
           "cte_corr_crypto AS ( " \
           "SELECT round_time_5m(\"creationtime\" AT TIME ZONE 'UTC') hour_beginning_eth, AVG(\"adjclose\") avg_value_eth " \
           "FROM \"btctickerdata\" " \
           "WHERE \"creationtime\" AT TIME ZONE 'UTC' IS NOT NULL " \
           "GROUP BY round_time_5m(\"creationtime\" AT TIME ZONE 'UTC') " \
           "ORDER BY round_time_5m(\"creationtime\" AT TIME ZONE 'UTC') ASC) " \
           "SELECT cte_corr_crypto.hour_beginning_eth AS creationtime, CAST (cte_corr_crypto.avg_value_eth AS INTEGER) AS open, CAST (cte_corr_crypto.avg_value_eth AS INTEGER) AS HIGH, CAST (cte_corr_crypto.avg_value_eth AS INTEGER) AS LOW, CAST (cte_corr_crypto.avg_value_eth AS INTEGER) AS VOLUME, CAST (cte_corr_crypto.avg_value_eth AS INTEGER) AS CLOSE " \
           "FROM cte_corr_crypto INNER JOIN cte_ratio ON cte_ratio.tm = cte_corr_crypto.hour_beginning_eth;"


data_count = DbConnectExec(runquery)
print(data_count)

query = "TRUNCATE TABLE tempsentiment;"

data_count = DbConnectExec(query)
print(data_count)

runquery = "INSERT INTO tempSentiment (creationtime,open,high,low,volume,close) " \
           "WITH cte_bullish AS ( " \
           "SELECT round_time_5m(\"Creationtime\") hour_beginning, COUNT(\"Sentiment\") bullish_count   " \
           "FROM \"twittertweetsentimentn\" " \
           "WHERE \"Creationtime\" IS NOT NULL  " \
           "AND \"Sentiment\" = 1   " \
           "GROUP BY round_time_5m(\"Creationtime\")    " \
           "ORDER BY round_time_5m(\"Creationtime\") ASC), " \
           "cte_bearish AS (    " \
           "SELECT round_time_5m(\"Creationtime\") hour_beginning, COUNT(\"Sentiment\") bearish_count   " \
           "FROM \"twittertweetsentimentn\" " \
           "WHERE \"Creationtime\" IS NOT NULL  " \
           "AND \"Sentiment\" = -1  " \
           "GROUP BY round_time_5m(\"Creationtime\")    " \
           "ORDER BY round_time_5m(\"Creationtime\") ASC),  " \
           "cte_ratio AS (  " \
           "SELECT cte_bearish.hour_beginning tm, round(cte_bullish.bullish_count / cte_bearish.bearish_count::numeric, 2) AS ratio " \
           "FROM cte_bearish INNER JOIN cte_bullish ON cte_bullish.hour_beginning = cte_bearish.hour_beginning),    " \
           "cte_corr_crypto AS (    " \
           "SELECT round_time_5m(\"creationtime\" AT TIME ZONE 'UTC') hour_beginning_eth, AVG(\"adjclose\") avg_value_eth   " \
           "FROM \"btctickerdata\"  " \
           "WHERE \"creationtime\" AT TIME ZONE 'UTC' IS NOT NULL   " \
           "GROUP BY round_time_5m(\"creationtime\" AT TIME ZONE 'UTC') " \
           "ORDER BY round_time_5m(\"creationtime\" AT TIME ZONE 'UTC') ASC)    " \
           "SELECT cte_ratio.tm AS creationtime, cte_ratio.ratio AS open, cte_ratio.ratio AS HIGH, cte_ratio.ratio AS LOW, cte_ratio.ratio AS VOLUME, cte_ratio.ratio AS CLOSE  " \
           "FROM cte_ratio INNER JOIN cte_corr_crypto ON cte_ratio.tm = cte_corr_crypto.hour_beginning_eth;"

data_count = DbConnectExec(runquery)
print(data_count)
