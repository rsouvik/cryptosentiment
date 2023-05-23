from sqlalchemy import create_engine


def postgresql(df, table):
    # Connect to the PostgreSQL server
    engine = create_engine(f'postgresql+psycopg2://sray:@localhost:5432/mycooldb')
    # df.to_csv("test.csv")
    # Send dataframe to PostgreSQL table in database. Replace, if already exist
    df.to_sql(table, engine, if_exists='replace', index=False)

    return df
