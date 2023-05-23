import pandas as pd
import tokenizer as tokenizer
import tweepy
import datetime

import nltk

nltk.download("stopwords")
nltk.download("wordnet")
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english", ignore_stopwords=False)
lemmatizer = WordNetLemmatizer()

# text = ""
# tokenized_text = tokenizer.tokenize(text.lower())
# words = [lemmatizer.lemmatize(w) for w in tokenized_text if w not in stop_words]
# stemming
# stem_text = "".join([stemmer.stem(i) for i in words])

ACCESS_TOKEN = '18773065-0ks7vqVxS6GDtvhHi19xGPyomqjoqTKmKygAAjxSg'
ACCESS_SECRET = 'cs5KxmGxAujwc09XCHfoukwc9Af1E3yMvQtnRutHcyXLF'
CONSUMER_KEY = '1L5uNCD1gV4sF3sslfsaYUUbH'
CONSUMER_SECRET = 'QVrWkkXaQlqJZHp92Jiv6wItwvlh9grbKp1cQBKOTqWnxZi9qm'


# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


class SAT:
    api = connect_to_twitter_OAuth()

    def mine_crypto_currency_tweets(self, query="bitcoin"):

        last_tweet_id = False
        page_num = 1

        data = pd.DataFrame()
        cypto_query = f"#{query}"
        print(" ===== ", query, cypto_query)
        for page in tweepy.Cursor(
                self.api.search_tweets,
                q=cypto_query,
                lang="en",
                tweet_mode="extended",
                count=10,
        ).pages(1):
            print(" ...... new page", page_num)
            page_num += 1

            for item in page:
                mined = {
                    "tweet_id": item.id,
                    "name": item.user.name,
                    "screen_name": item.user.screen_name,
                    "retweet_count": item.retweet_count,
                    "text": item.full_text,
                    "mined_at": datetime.datetime.now(),
                    "created_at": item.created_at,
                    "favourite_count": item.favorite_count,
                    "hashtags": item.entities["hashtags"],
                    "status_count": item.user.statuses_count,
                    "followers_count": item.user.followers_count,
                    "location": item.place,
                    "source_device": item.source,
                    "tweet_end": "--------####--------"
                }

                try:
                    mined["retweet_text"] = item.retweeted_status.full_text

                    """
                    text = "bitcoin will go up"
                    tokenized_text = tokenizer.tokenize(text.lower())
                    words = [lemmatizer.lemmatize(w) for w in tokenized_text if w not in stop_words]
                    # stemming
                    stem_text = "".join([stemmer.stem(i) for i in words])
                    analysis = TextBlob(stem_text)
                    print("sat score for stemmed text is ", analysis.sentiment.polarity)
                    """

                except:
                    mined["retweet_text"] = "None"

                print("Tweet is: ", mined["text"])
                testimonial = TextBlob(mined["text"])
                print(testimonial.sentiment)

                last_tweet_id = item.id
                data = data.append(mined, ignore_index=True)
                # data = data.append(mined["text"])
                # row = pd.DataFrame({'Text': [mined["text"]]})
                # pd.concat([data, row])

            if page_num % 180 == 0:
                date_label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                print("....... outputting to csv", page_num, len(data))
                data.to_csv(f"{query}_{page_num}_{date_label}.csv", index=False)
                print("  ..... resetting df")
                """data = get_df()"""
                data = pd.DataFrame()

        date_label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        data.to_csv(f"{query}_{page_num}_{date_label}.csv", index=False)


if __name__ == "__main__":
    hftd = SAT()
    hftd.mine_crypto_currency_tweets()
