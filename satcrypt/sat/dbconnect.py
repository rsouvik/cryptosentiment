# Connecting to the Database
import psycopg2


def DbConnect(query):
    conn = psycopg2.connect(host="localhost", database="mycooldb", port=5432, user="sray", password="")
    curr = conn.cursor()

    curr.execute(query)

    rows = curr.fetchall()

    return rows


def DbConnectExec(query):
    conn = None
    rows_deleted = 0
    try:
        conn = psycopg2.connect(host="localhost", database="mycooldb", port=5432, user="sray", password="")
        curr = conn.cursor()

        curr.execute(query)
        rows_deleted = curr.rowcount
        conn.commit()
        curr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted

