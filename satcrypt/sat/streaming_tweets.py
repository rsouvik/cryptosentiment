# Streaming tweets
import tweepy

from sat.authenticate_twitter_api import api
from sat.tweetStreamListener import MyStreamListener

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener,
                         tweet_mode="extended")
# myStream.filter(track=['crypto', 'btc', 'bitcoin', 'nft', 'blockchain', 'ethereum'])
myStream.filter(track=['#btc', '#bitcoin'])
# myStream.filter(track=['#eth', '#ethereum'])
# myStream.filter(track=['#btc', '#bitcoin', 'crypto', 'btc', 'bitcoin', 'nft', 'blockchain', 'ethereum'],
# myStream.filter(follow=['295218901', '1469101279', '139487079', '2362854624', '176758255', '339061487', '14379660',
#                      '396045469',
#                     '244647486', '20884310', '14338147', '44196397'])

# myStream.filter(
#  track=['#cryptocoin', '#bitcoinusa', '#cryptoworld', '#coinbasewallet', '#cryptotrading', '#bitcoincash',
#        '#bitcoin', '#cryptocurrencies', '#blockchain', '#crypto'])
