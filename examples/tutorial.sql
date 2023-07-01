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
    year INT,
    p_event VARCHAR(255),  
    PRIMARY KEY(id) 
);
