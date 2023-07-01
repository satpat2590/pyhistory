'''
Providing a way to interact with the MySQL DB!
'''
import mysql.connector
from mysql.connector import Error


def add_to_events(ctx, value):
    insert = f"INSERT INTO events (eventname, year, p_event) VALUES {value}"
    cursor = ctx.cursor()
    cursor.execute(insert)
    print_events(ctx)

def print_events(ctx):
    eventlist = f"SELECT * FROM events" 
    cursor = ctx.cursor()
    cursor.execute(eventlist)
    print(f"\n\nThis is the final table from host_testing/models/events.py: {cursor.fetchall()}")

