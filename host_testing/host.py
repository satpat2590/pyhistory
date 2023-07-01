import mysql.connector as sqlc
from mysql.connector import Error 
import models.events as sqlinterface
import os 
from dotenv import load_dotenv

try: 

    load_dotenv()
    ctx = sqlc.connect(
        username=os.environ["USERNAME"],
        password=os.environ["PASSWORD"],
        database=os.environ["DATABASE"]
    )
    query_tables = f"SHOW TABLES"
    cursor = ctx.cursor() 
    cursor.execute(query_tables)
    tablelist = [x[0] for x in cursor.fetchall()]
    print(f"Printing out available tables: {tablelist}")
    table_val = ('Satyams Birth', 2000, 'Beginning of 21st century')

    insert = f"INSERT INTO {tablelist[0]} (eventname, year, p_event) VALUES {table_val}"
    cursor.execute(insert)
    query = f"SELECT * FROM {tablelist[0]}"
    cursor.execute(query)
    print(f"Query results: \n{cursor.fetchall()}")

    tuple_ex = ("Howdy", 2000, "Goodbye", 65788)
    table_val2 = ('Satyams Birth', 2000, 'Birth of Jesus')
    cursor.execute(f"DESCRIBE {tablelist[0]}")
    table_attr = [x[0] for x in cursor.fetchall()]

    print("\n", tuple(table_attr), table_val2)
    sqlinterface.add_to_events(ctx, table_val2)





except Error as e: 
    print(f"\nUnable to connect to the MySQL DB...\nError log:\n\t{e}")

finally:
    if ctx.is_connected():
        ctx.commit()
    print(f"\nClosing the database...\n")
    ctx.close() 