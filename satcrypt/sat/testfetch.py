from sat.fetch_sentiment_for_range import fetch

df = fetch("select 'Sentiment' from twittertweetsentimentn where 'Creationtime' > '2022-05-02 13:59:00'")
print(df.head())