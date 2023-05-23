# Twitter API authentication

import tweepy

from sat.satcreds import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_TOKEN

api_key = CONSUMER_KEY
api_secret_key = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_SECRET

# authorize the API Key
authentication = tweepy.OAuthHandler(api_key, api_secret_key)

# authorization to user's access token and access token secret
authentication.set_access_token(access_token, access_token_secret)

# call the api
api = tweepy.API(authentication)
