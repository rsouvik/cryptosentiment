# Twitter package imports
import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream

import matplotlib.pyplot as plt

# Sentiment Analysis library
from textblob import TextBlob

from satcreds import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

# Helpful packages for data and plotting
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

#Twitter authentication

# extract tweets, clean them and store with timestamp into db
# then run textblob to generate the sentiment scores

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        return auth

class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(languages='en', track=hash_tag_list)


##########____TWITTER STREAM LISTENER____#############
class TwitterListener(tweepy.Stream):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


###########____TWEET ANALYZER____############
class TweetAnalyzer():
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_search_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.search_tweets, until='2022-01-19', q='Bitcoin').items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_follower_list(self, num_followers):
        follower_list = []
        for follower in Cursor(self.twitter_client.followers, id=self.twitter_user).items(num_followers):
            follower_list.append(follower)
        return follower_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()
    #tweets = api.user_timeline(screen_name="mimistic02", count=200)
    tweets = twitter_client.get_search_timeline_tweets(100)

    # print(dir(tweets[0]))
    # print(tweets[0].retweet_count)

    # Analyze sentiment
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    print(df.shape)

    #df.plot(x="id", y=["sentiment"])
    #plt.show()

    # print(df.head(10))
    # Get average length over all tweets:
    print(np.mean(df['len']))

    # Get the number of likes for the most liked tweet:
    print(np.max(df['likes']))
    # Get the number of retweets for the most retweeted tweet:
    print(np.max(df['retweets']))

    # Layered Time Series Plot
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    #time_sentiment.plot(figsize=(16, 4), label="sentiment", legend=True)
    #plt.show()

    sent_column = df["sentiment"]
    sent_column.plot(kind="hist")
    plt.show()

    # # Option to use cursor with Twitter Client for specific API references
    # twitter_client = TwitterClient('user_screen_name')
    # print(twitter_client.get_user_timeline_tweets(1))

    # # Option to stream topic list and save to json
    # hash_tag_list = ["Trump", "Covid-19", "coronavirus", "WHO"]
    # fetched_tweets_filename = "tweets.json"
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)