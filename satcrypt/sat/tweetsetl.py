# Insert Tweet data into database
import psycopg2
import pandas as pd

from sat.utils import datetime_from_utc_to_local


def dbConnect(user_id, user_name, tweet_id, tweet, retweet_count, hashtags, t_time):
    conn = psycopg2.connect(host="localhost", database="mycooldb", port=5432, user="sray", password="")

    cur = conn.cursor()
    #tweet_time = datetime_from_utc_to_local(t_time)
    tweet_time = t_time

    # insert user information
    command = '''INSERT INTO TwitterUser (user_id, user_name) VALUES (%s,%s) ON CONFLICT
                 (User_Id) DO NOTHING;'''
    cur.execute(command, (user_id, user_name))

    # insert tweet information
    command = '''INSERT INTO TwitterTweet (tweet_id, user_id, tweet, retweet_count, creationtime) VALUES (%s,%s,%s,%s,%s);'''
    cur.execute(command, (tweet_id, user_id, tweet, retweet_count, tweet_time))

    # insert entity information
    for i in range(len(hashtags)):
        hashtag = hashtags[i]
        command = '''INSERT INTO TwitterEntity (tweet_id, hashtag) VALUES (%s,%s);'''
        cur.execute(command, (tweet_id, hashtag))

    # Commit changes
    conn.commit()

    # Disconnect
    cur.close()
    conn.close()


def dbConnectCrypto(ctime, open_price, high_price, low_price, close_price, adjclose_price, volume):
    conn = psycopg2.connect(host="localhost", database="mycooldb", port=5432, user="sray", password="")

    cur = conn.cursor()

    # insert user information
    command = '''INSERT INTO BtcTickerData (Creationtime, OpenPrice, HighPrice, LowPrice, ClosePrice, AdjClose, Volume) 
                 VALUES (%s,%s,%s,%s,%s,%s,%s);'''
    cur.execute(command, (ctime, open_price, high_price, low_price, close_price, adjclose_price, volume))

    # Commit changes
    conn.commit()

    # Disconnect
    cur.close()
    conn.close()


def postgresql_to_dataframe(select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """

    conn = psycopg2.connect(host="localhost", database="mycooldb", port=5432, user="sray", password="")
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    # Naturally we get a list of tupples
    tuples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tuples, columns=column_names)
    return df
