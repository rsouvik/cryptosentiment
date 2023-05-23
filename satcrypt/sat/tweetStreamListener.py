import time

import tweepy

from sat.hashtags import read_hashtags
from sat.tweetsetl import dbConnect


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, time_limit=480):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener, self).__init__()

    def on_connect(self):
        print("Connected to Twitter API.")

    def on_status(self, status):

        # Timestamp
        tweet_time = status.created_at
        # Tweet ID
        tweet_id = status.id

        # User ID
        user_id = status.user.id
        # Username
        username = status.user.name

        # Tweet
        if status.truncated == True:
            tweet = status.extended_tweet['full_text']
            hashtags = status.extended_tweet['entities']['hashtags']
        else:
            tweet = status.text
            hashtags = status.entities['hashtags']

        # Read hastags
        hashtags = read_hashtags(hashtags)

        # Retweet count
        retweet_count = status.retweet_count
        # Language
        lang = status.lang

        # If tweet is not a retweet and tweet is in English
        if not hasattr(status, "retweeted_status") and lang == "en":
            #Connect to database
            #print(tweet_time)
            dbConnect(user_id, username, tweet_id, tweet, retweet_count, hashtags, tweet_time)
            #print(tweet_time)

        if (time.time() - self.start_time) > self.limit:
            print(time.time(), self.start_time, self.limit)
            return False

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False
