import mysql.connector 
from mysql.connector import Error
import os.path
import langchain 
from langchain import PromptTemplate, LLMChain 
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class DatabaseMgmt():
    def __init__(self, connection):
        self.connection = connection
        print("Connection is successfully stored!\n")
    
    def print_dbs(self):
        cursor = self.connection.cursor() # initialize the SQL command executor
        cursor.execute("select database()")
        # fetchone() method returns an array of databases, automatically using the first one 
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name[0]}") # Print out first database in list
    
    def server_info(self): 
        # get_server_info() retrieves the server details (which is your personal computer or cloud)
        table_info = self.connection.get_server_info()
        print(f"Here's the server info: {table_info}")

    def print_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("show tables")
        tables = cursor.fetchall()
        if tables:
            print(f"There is a table within the database: {tables[0][0]}\n")
        else:
            print(f"There are NO tables within the database selected\n") 

    def describe_table(self, table):
        cursor = self.connection.cursor()
        cursor.execute(f"describe {table}")
        print(f"{cursor.fetchall()}")

    def insert_data(self, events):
        try:
            cursor = self.connection.cursor()
            for i, y, e, d, p in events: 
                if (p == None):
                    cursor.execute(f"insert into events (year, eventname, description) values ({y}, '{e}', '{d}')")
                    print("inserted without parent event...\n")
                else:
                    cursor.execute(f"insert into events (year, eventname, description, p_event) values ({y}, '{e}', '{d}', '{p}')")
                    print("inserted with parent event...\n")
        except Error: 
            print(f"Event '{e}' already exists within the database, stopping...\n")

    def modify_event(self, event, column, value):
        update_format = f"update events set {column} = '{value}' where eventname = '{event}'"
        cursor = self.connection.cursor()
        cursor.execute(update_format)
        # retrieve event to make sure it's correct
        cursor.execute(f"select * from events where eventname = '{event}'")
        print(f"\nModified Row: {cursor.fetchone()}\n")
        
    def show_events(self):
        cursor = self.connection.cursor() 
        cursor.execute("select * from events")
        events = cursor.fetchall()
        for event in events: 
            print(f"{event}\n")

    def chain_of_events(self, event, list=None):
        """
        Returning the 'chain of events' which led to the event parameter occurring.

        For example, if 'Birth of Christ' is passed as the event, then it will find 
        all parent events, grandparent events, ..., until an event returns with no parent event (singularity event)
        """
        if list is None:
            list = []

        cursor = self.connection.cursor()

        if isinstance(event, str):  # if it's a string
            cursor.execute("SELECT * FROM events WHERE eventname = %s", (event,))
            e = cursor.fetchone()
        else:  # if it's a tuple
            e = event

        if e[4] == None: # if parent event is None, then terminate program
            list.append(e)
            return list[::-1] # return reversed list
        else:
            cursor.execute("select * from events where eventname = %s", (e[4],))
            p_e = cursor.fetchone()
            list.append(e)
            return self.chain_of_events(p_e, list)


def get_chain(db, event):
    events = db.chain_of_events(event)
    print(events)
    for event in events:
        if event[2] < 0:
            print(f"{event[1]} - {abs(event[2])} B.C\n")
        else:
            print(f"{event[1]} - {event[2]} A.D\n") 


i_events0 = [
    (None, -3300, "Start of Indus Valley Civilization", "The Indus Valley Civilization, also known as the Harappan Civilization, began to develop in the northwestern region of the Indian subcontinent. It is notable for its advanced urban planning and architecture.", None),
    (None, -2600, "Urbanization in Indus Valley", "The urban phase of the Indus Valley Civilization began, marked by the development of cities like Harappa, Mohenjo-daro, and Lothal. These cities were characterized by well-planned streets, advanced drainage systems, and impressive architecture.", "Start of Indus Valley Civilization"),
    (None, -2500, "Standardized weights and measures", "The use of standardized weights and measures across the civilization, as evidenced by uniformly cut bricks and standardized scales, points towards a complex economic system.", "Urbanization in Indus Valley"),
    (None, -1900, "Decline of Indus Valley Civilization", "The Indus Valley Civilization began to decline for reasons that are still debated among historians. Various theories include climate change, overpopulation, and invasion or internal conflict.", "Standardized weights and measures"),
    (None, -1500, "End of Indus Valley Civilization", "The Indus Valley Civilization came to an end, transitioning into the Vedic period. The exact reasons behind this decline and transition remain a matter of scholarly debate.", "Decline of Indus Valley Civilization"),
]

i_events1 = [
    (None, -2000, "Indo-Iranian migration", "The Indo-Iranians, a branch of the Indo-European language family, started migrating from the Eurasian Steppes to the Indian subcontinent. This migration greatly influenced the language and culture of the region.", None),
    (None, -1500, "Vedic period", "This period marked the composition of the Vedas, the oldest scriptures of Hinduism. Society was organized around four Varnas, or classes, and the concepts of Dharma and Karma emerged.", "Indo-Iranian migration"),
    (None, -600, "Mahajanapadas", "This period saw the rise of 16 large states, or `Mahajanapadas`, in the northern Indian subcontinent. It was a time of significant political, economic, and cultural development.", "Vedic period"),
    (None, -528, "Enlightenment of Buddha", "During this time, Siddhartha Gautama, later known as Buddha, achieved enlightenment and began teaching the principles of Buddhism, leading to its spread throughout and beyond India.", "Mahajanapadas"),
    (None, -327, "Alexander`s invasion of India", "Alexander the Great extended his empire into northwest India. Although short-lived, this invasion opened routes for future Indo-Greek relations.", "Mahajanapadas"),
    (None, -322, "Start of Maurya Empire", "Chandragupta Maurya, aided by his advisor Chanakya, overthrew the Nanda Dynasty and established the Maurya Empire, marking the start of a politically unified India.", "Alexander`s invasion of India"),
    (None, -273, "Ashoka`s reign", "Emperor Ashoka ruled the Maurya Empire, expanding it to include nearly the entire Indian subcontinent. After the Kalinga war, he converted to Buddhism and propagated its principles throughout his empire.", "Start of Maurya Empire"),
    (None, -232, "Death of Ashoka", "Emperor Ashoka`s death led to the fragmentation and decline of the Maurya Empire. His influence, however, notably his role in spreading Buddhism, had lasting global impact.", "Ashoka`s reign"),
    (None, -185, "Start of Shunga Empire", "The Shunga Empire arose in Magadha following the fall of the Maurya Empire. While they faced numerous challenges, the Shungas managed to promote cultural activities and the fine arts.", "Death of Ashoka"),
    (None, -150, "Start of Satavahana dynasty", "The Satavahana dynasty was established in Deccan India after the decline of the Maurya Empire. The Satavahanas are noted for their patronage of Hinduism and Buddhism, and for their contributions to art and architecture.", "Start of Shunga Empire"),
]

i_events2 = [
    (None, -110, "Fall of the Shunga Empire", "The Shunga Empire, which saw significant cultural and artistic growth, ended. The end of this empire marked the beginning of a period of instability before the rise of the Gupta Empire.", "Start of Shunga Empire"),
    (None, 78, "Start of Kushan Empire", "The Kushan Empire was established by Kujula Kadphises. It played a key role in the Silk Road trade network and the spread of Buddhism to China.", "Alexander`s invasion of India"),
    (None, 320, "Start of Gupta Empire", "The Gupta Empire, often referred to as the Golden Age of India, was established. This period is celebrated for its advancements in arts, science, philosophy, and architecture.", "Fall of the Shunga Empire"),
    (None, 375, "Reign of Chandragupta II", "Chandragupta II, also known as Vikramaditya, was one of the most powerful emperors of the Gupta Empire. His reign saw significant cultural and academic advancements, including the work of the famous poet and scholar Kalidasa.", "Start of Gupta Empire"),
    (None, 450, "Invasions by the Huna", "The Huna people, also known as the Huns, conducted several invasions into Gupta territory. These invasions led to a decline in the Gupta Empire`s power and marked the beginning of a period of political instability in northern India.", "Reign of Chandragupta II"),
    (None, 600, "Harsha`s Reign", "Harsha, also known as Harshavardhana, ruled much of North India from 606 to 647 CE. His reign is often celebrated for its cultural and religious tolerance, patronage of arts, and efforts to establish educational institutions.", "Invasions by the Huna"),
    (None, 712, "Arab Conquest of Sindh", "Muhammad bin Qasim, an Arab general, conquered Sindh and parts of Punjab, marking the start of Islamic rule in parts of the Indian subcontinent.", "Harsha`s Reign"),
    (None, 750, "Start of Pala Empire", "The Pala Empire, the last major Buddhist imperial power in India, was established by Gopala in the region of Bengal. The Pala dynasty is known for its patronage of Buddhism and contributions to art, sculpture, and architecture.", "Arab Conquest of Sindh"),
    (None, 800, "Start of Rashtrakuta Empire", "The Rashtrakuta Empire was established in the Deccan plateau region of India. Known for their architectural contributions, including the Kailasa Temple at Ellora.", "Start of Pala Empire"),
    (None, 985, "Start of Chola Empire", "Rajaraja Chola I ascended the throne, marking the start of the Chola Empire in southern India. The Cholas left a remarkable artistic legacy, including the magnificent Brihadeeswarar Temple.", "Start of Rashtrakuta Empire"),
]



# Always put database connections within an exception handling block!
try: 
    # Using the connect() method with user details. 
    # Be sure to place all passwords and user info within an .env file!  
    connection = mysql.connector.connect(
        host='db',
        user='root',
        password='password',
        database='history'
    )

    # Run following code ONLY IF successfully connected to database
    if connection.is_connected():
        db = DatabaseMgmt(connection) # initialize DatabaseMgmt
        db.server_info() # get server information 
        #db.print_dbs() # print the available databases
        #db.print_tables() # print out all of the available tables in selected database
        #db.insert_data(i_events0)
        #db.show_events()
        #db.modify_event("Indo-Iranian migration", "p_event", "End of Indus Valley Civilization")
        get_chain(db, "Start of Rashtrakuta Empire")


# If any exception/error is thrown within the try block, automatically jump here... 
except Error as e: 
    print(f"Error connecting to the MySQL database\nError log: \t{e}")
    
# Mandatory block of code to run whenever either the try block finishes or exception is handled. 
finally: 
    if connection.is_connected():
        connection.commit()
        connection.close()
        print("MySQL connection is closed\n") 