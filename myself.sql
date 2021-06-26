CREATE DATABASE myself;

CREATE TABLE skills(
	Name varchar(255),
    Time int,
    TimeUnit varchar(255)
);

CREATE TABLE workexperience(
	Name varchar(255),
    Duration int,
    DurationUnit int,
    Organization varchar(255),
    Salary float,
    WHours float
);

CREATE TABLE volunteerexperience(
	Name varchar(255),
    Duration int,
    DurationUnit int,
    Organization varchar(255),
    WHours float
);

CREATE TABLE projects(
	Name varchar(255),
    Description varchar(255)
);

INSERT INTO skills (Name, Time, TimeUnit)
VALUES ('Python', 2, 'Year');
INSERT INTO skills (Name, Time, TimeUnit)
VALUES ('Java', 2, 'Year');
INSERT INTO skills (Name, Time, TimeUnit)
VALUES ('C++', 2, 'Year');
INSERT INTO skills (Name, Time, TimeUnit)
VALUES ('C', 2, 'Year');

SELECT * FROM skills;