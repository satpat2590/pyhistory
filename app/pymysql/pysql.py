import mysql.connector 
from mysql.connector import Error
import os.path
import langchain 
import openai  
from langchain import PromptTemplate, LLMChain 
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler



# Always put database connections within an exception handling block!
try: 
    # Using the connect() method with user details. 
    # Be sure to place all passwords and user info within an .env file!  
    #connection = mysql.connector.connect(host=os.environ["MYSQL_HOST_TEST"], database=os.environ["MYSQL_DATABASE_TEST"], user=os.environ["MYSQL_USER_TEST"], password=os.environ["MYSQL_PASSWORD_TEST"])
    connection = mysql.connector.connect(
        host='db',
        user='root',
        password='password',
        database='history'
    )
    # Run following code ONLY IF successfully connected to database
    if connection.is_connected():
        # get_server_info() retrieves the server details (which is your personal computer or cloud)
        table_info = connection.get_server_info()
        print(f"Here's the server info: {table_info}")
        
        # Create a cursor (similar to 'prepared statements') which can execute MySQL commands 
        cursor = connection.cursor()
        # Returns a list of available databases 
        cursor.execute("select database();")
        # fetchone() method returns an array of databases, automatically using the first one 
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name[0]}") # Print out first database in list
        cursor.execute("SHOW TABLES")
        print(f"These are the available tables: {cursor.fetchall()}")
        if cursor.fetchall():
            print(f"There is a table within the database! Here: {cursor.fetchall()}\n\tThe type of cursor return: {type(cursor.fetchall())}\n")
        else:
            print(f"There are NO tables within the database selected\n") 
        #cursor.execute("SELECT * FROM example")
        # fetchall() method returns all of the resultant rows and stores within 'result' 
        #result = cursor.fetchall()
        #print(f"This is our final printed table:\n")
        # Resultant set stored as array of tuples (# of tuples depends on # of columns)
        #for w, x, y, z in result: 
            #print(f"Age: {w}\nFirst Name: {x}\nLast Name: {y}\nEmail: {z}\n\n\n")


# If any exception/error is thrown within the try block, automatically jump here... 
except Error as e: 
    print(f"Error connecting to the MySQL database\nError log: \t{e}")
    
# Mandatory block of code to run whenever either the try block finishes or exception is handled. 
finally: 
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed\n") 