from sat.tweetsetl import postgresql_to_dataframe

"""column_names = ["User_Id", "Tweet_Id", "Tweet", "Retweet_Count", "Creationtime", "Clean_Tweet", "Sentiment"]
df = postgresql_to_dataframe("select * from twittertweetsentimentn where 'Creationtime' > '2022-05-02 13:59:00' ", column_names)
print(df["Sentiment"])
"""

# column_names = ["creationtime", "openprice", "highprice", "lowprice", "closeprice", "volume", "adjclose"]
column_names = ["Open", "High", "Low", "Close", "Volume"]
df = postgresql_to_dataframe("select adjclose,adjclose,adjclose,adjclose,adjclose from btctickerdata where 'Creationtime' > '2022-05-02 13:59:00' ", column_names)
print(df)
