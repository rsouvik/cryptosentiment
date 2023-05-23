# Table creation
commands = (
    # Table 2
    '''Create Table TwitterTweetSentiment(Tweet_Id BIGINT PRIMARY KEY,
                                 User_Id BIGINT,
                                 Tweet TEXT,
                                 Retweet_Count INT,
                                 Creationtime DATE,
                                 Sentiment INT,
                                 CONSTRAINT fk_user
                                     FOREIGN KEY(User_Id)
                                         REFERENCES TwitterUser(User_Id));''')