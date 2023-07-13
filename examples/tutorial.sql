CREATE DATABASE tutorial; 

USE tutorial; 

CREATE TABLE users (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255), 
    email VARCHAR(255),  
    PRIMARY KEY(id) 
)

CREATE TABLE purchases (
    id MEDIUMINT NOT NULL AUTO_INCREMENT, 
    itemname VARCHAR(255) NOT NULL,
    user_id MEDIUMINT, 
    PRIMARY KEY(id) 
)


CREATE TABLE events (
    id MEDIUMINT NOT NULL AUTO_INCREMENT, 
    eventname VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    description TEXT NOT NULL, 
    p_event VARCHAR(255),  
    PRIMARY KEY(id), 
    UNIQUE (eventname)
);


TABLE events 
INTO OUTFILE '/var/lib/mysql-files/history.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ''
LINES TERMINATED BY '\n';


(SELECT 'columnHeading', ...)
UNION
(SELECT column, ...
FROM tableName
INTO OUTFILE 'path-to-file/outputFile.csv’'
FIELDS ENCLOSED BY '"' 
TERMINATED BY ','
ESCAPED BY '"'
LINES TERMINATED BY 'n')