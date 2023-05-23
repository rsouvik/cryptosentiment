from sat.tweetsetl import postgresql_to_dataframe


def fetch(query):
    # column_names = ["User_Id", "Tweet_Id", "Tweet", "Retweet_Count", "Creationtime", "Clean_Tweet", "Sentiment"]
    column_names = ["creationtime", "Open", "High", "Low", "Volume", "Close"]
    df = postgresql_to_dataframe(query, column_names)
    return df


def fetchBTC(query):
    # column_names = ["creationtime", "openprice", "highprice", "lowprice", "closeprice", "volume", "adjclose"]
    column_names = ["creationtime", "Open", "High", "Low", "Volume", "Close"]
    df = postgresql_to_dataframe(query, column_names)
    return df
