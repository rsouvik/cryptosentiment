# Create
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from sat.dbconnect import DbConnect
from sat.load_df_to_db import postgresql
from sat.preprocess_tweets import preprocess
from sat.tweet_sentiment import sentiment

data_tweet = DbConnect("SELECT User_Id, Tweet_Id, Tweet, Retweet_Count, Creationtime FROM TwitterTweet;")
#data_tweet = DbConnect("SELECT Tweet FROM TwitterTweet;")

df_tweet = pd.DataFrame(columns=['User_Id', 'Tweet_Id', 'Tweet', 'Retweet_Count', 'Creationtime', 'Clean_Tweet'])
#df_tweet = pd.DataFrame(columns=['Clean_Tweet'])


for data in data_tweet:
    index = len(df_tweet)
    df_tweet.loc[index, 'User_Id'] = data[0]
    df_tweet.loc[index, 'Tweet_Id'] = data[1]
    df_tweet.loc[index, 'Tweet'] = data[2]
    df_tweet.loc[index, 'Retweet_Count'] = data[3]
    df_tweet.loc[index, 'Creationtime'] = data[4]
    df_tweet.loc[index, 'Clean_Tweet'] = preprocess(data[2])

    #df_tweet.loc[index, 'Clean_Tweet'] = preprocess(data[0])

df_tweet['Sentiment'] = df_tweet['Clean_Tweet'].apply(sentiment)

dfn = postgresql(df_tweet, 'twittertweetsentimentn')

print(df_tweet.head(20))

#put into db. TBD

