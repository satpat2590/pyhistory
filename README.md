# pyhistory
Tackling through my long-anticipated history amalgamation through this stack: Python (Flask), MySQL, and Langchain!

## Overview:
In pursuing lofty ambitions, I decided to make this one particularly grand. I want to create a functional full-stack project which will 
use a MySQL database to store historical information: { event_name, year, synopsis, parent_event }. In doing so, I can envision a large collection of 
historical events and their significance in the grand scheme of time! 

To start, I'll have a basic application which is able to feed the database scheme to any LLM using Langchain (or LlamaIndex). The AI will 
then list out a bunch of events, making sure that all of the schema information is evident within the response itself. 

There will be an REST API developed which will allow anyone to perform CRUD operations to view the data on the frontend. However, a majority of
the data will be entered initially through functions which will call MySQL commands to perform CRUD operations. 



