from tokenize import tokenize

import tweepy
import json
import tokenizer

import nltk

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english", ignore_stopwords=True)
lemmatizer = WordNetLemmatizer()
text = "Very happy"
tokenized_text = word_tokenize(text.lower())
words = [lemmatizer.lemmatize(w) for w in tokenized_text if w not in stop_words]
# stemming
stem_text = "".join([stemmer.stem(i) for i in words])
analysis = TextBlob(stem_text)
print("sat score for stemmed text is ", analysis.sentiment)

#testimonial = TextBlob("BestChange — Collect free Satoshi BTC and learn e-currency exchange rates! Stable the faucet "
 #                      "to collect the cryptocurrency.")
testimonial = TextBlob("#Bitcoin could become reserve currency of the world.")
testimonial = TextBlob("Instantly move money to all corners of the world. @Ripple.")
testimonial = TextBlob("Ripple and Tranglo Singapore’s Partnership Scales to New Heights in Asia-Pacific")
print(testimonial.sentiment)
