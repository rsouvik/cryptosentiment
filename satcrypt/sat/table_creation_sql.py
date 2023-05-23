# Table creation
commands = (# Table 1
    '''Create Table TwitterUser(User_Id BIGINT PRIMARY KEY, User_Name TEXT);''',
    # Table 2
    '''Create Table TwitterTweet(Tweet_Id BIGINT PRIMARY KEY,
                                 User_Id BIGINT,
                                 Tweet TEXT,
                                 Retweet_Count INT,
                                 Creationtime DATE,
                                 CONSTRAINT fk_user
                                     FOREIGN KEY(User_Id)
                                         REFERENCES TwitterUser(User_Id));''',
    # Table 3
    '''Create Table TwitterEntity(Id SERIAL PRIMARY KEY,
                                 Tweet_Id BIGINT,
                                 Hashtag TEXT,
                                 CONSTRAINT fk_user
                                     FOREIGN KEY(Tweet_Id)
                                         REFERENCES TwitterTweet(Tweet_Id));''')