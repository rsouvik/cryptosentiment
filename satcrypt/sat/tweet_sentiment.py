# Sentiment analysis using Textblob
from textblob import TextBlob


def sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

#df_tweet['Sentiment'] = df_tweet['Clean_Tweet'].apply(sentiment)

#df_tweet.head(20)
