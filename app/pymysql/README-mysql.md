# MySQL Practice Tutorial!

## Setting up MySQL (For use with Docker!)

If you don't wish to download MySQL on your host computer and save that memory and headache, no worries! This repository contains a file pyhistory/docker-compose.yml which 
handles multiple 'services' which is a fancy way of calling it a 'docker image which is fine-tuned and placed on a custom network'. 

The capabilities are quite amazing! You can connect a MySQL docker container with a Python docker container with a Node docker container and then essentially build your
tech stack altogether. This is much MUCH better (or not) than having to initialize a docker image for a base OS such as Ubuntu and having to manually download each package to suit your build. 

Follow the steps listed in the base pyhistory/README.md in order to run the various docker containers and set up your MySQL!

## Setting up MySQL (On Host Computer!)

You can go on the MySQL website and find a debian package if you're running this on a debian machine such as Linux/Ubuntu. If not, there should be examples online to find easily downloadable versions for both Windows and Mac

### Ubuntu/Debian based systems 

1. Get the debian package for MySQL 

2. Run the following bash line to download and install the MySQL debian package

```bash
sudo apt deb [package-name].deb
```

3. Once downloaded, follow the steps to set up your MySQL as well as the daemon (configures and runs the MySQL service as a process on your computer) 

4. Follow the steps to either create a new user or keep root privileges, and either assign a password or choose to keep none. 

5. Once you've configured the initial setup of MySQL, you can begin to run the command line interface by simply running the following: 

```bash
mysql -u root -p 
```

Which should then prompt you to enter the password in a secure manner. Once done, you've finally entered the MySQL command line interface! 

## Common Commands for the CLI 

### Creating a new Database
- CREATE DATABASE [enter name of your database];

### Dropping a Database
- DROP DATABASE [enter name of your database]; 

### Using a Database (selecting into it)
- USE DATABASE [enter name of your database]; 

### Creating a Table within a Database
- CREATE TABLE [enter table name] (
    column-name DATATYPE, 
    column-name DATATYPE,
    ...
)

### Querying a Table(s) within a Database
- SELECT [insert comma separated column names..] FROM [enter table name] 

#### Conditional querying
- SELECT [insert comma separated column names..] FROM [enter table name] WHERE [column name] = [value of column] 

#### Join querying
- SELECT [insert comma separated column names..] 
FROM [table1] 
INNER JOIN [table2] 
ON table1.[enter column name here] = table2.[enter column name here]

NOTE: Inner Join is essentially an intersection operation between two sets. If the condition specified with the 'ON' keyword is fulfilled on both ends, then those rows will be present within the final resultant set

- SELECT [insert comma separated column names..] 
FROM [table1] 
LEFT JOIN [table2] 
ON table1.[enter column name here] = table2.[enter column name here]

NOTE: In a left join, all of the rows from the left table (table1 in this example) are present within the resultant set. However, only those that fulfill the condition specified are added to the resultant set from table2. If no rows pass the conditions within table2, then no rows are joined and only table1 is shown. 

- SELECT [insert comma separated column names..] 
FROM [table1] 
LEFT JOIN [table2] 
ON table1.[enter column name here] = table2.[enter column name here]

NOTE: *OPPOSITE OF LEFT JOIN (DUH!!!)* In a right join, all of the rows from the right table (table2 in this example) are present within the resultant set. However, only those that fulfill the condition specified are added to the resultant set from table1. If no rows pass the conditions within table1, then no rows are joined and only table2 is shown. 






