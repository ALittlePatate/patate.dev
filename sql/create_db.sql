CREATE DATABASE guestbook;
USE guestbook;

CREATE TABLE guestbook (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    message TEXT
);
