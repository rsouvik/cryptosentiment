# Create cursor to execute SQL commands
import psycopg2
from sat.table_creation_sql import commands

conn = psycopg2.connect(host="localhost",database="mycooldb",port=5432,user="sray",password="")

cur = conn.cursor()

# Execute SQL commands
for command in commands:
    # Create tables
    cur.execute(command)

# Close communication with server
conn.commit()
cur.close()
conn.close()