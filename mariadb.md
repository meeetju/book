# MariaDB cheat sheet

## References

[MadiaDB](https://mariadb.com/)

[Sample databases](https://dev.mysql.com/doc/index-other.html)

> Note: To import the database in `dBeaver` select the database, pick `SQL Editor` -> `New SQL Script` then copy there content of `schema.sql` file and run `Execute SQL script`, then do the same with `data.sql` file. Note the script has to have `<localhost>` in the tab title.

## General

Relational database management system which has resemblence to MySQL.

- Relational database is when two or more tables are related.
- `RDBMS` is a Relational Database Management System
  - For example `dBeaver`
- `Primary key` is used to uniquely identify each record in a database. It can't have a `null` value. A table may have only one primary key which may consist of a single or multiple fields.
- `Foreign key` is used to link two tables together. It is a key in one table that is a `Primary key` in another table. It may consist of a single or multiple fields.
- A table which consist of a `Primary key` is a parent table.
- A table which consist of a `Foreign key` is a child table.
- `Constraints` are used to specify the rules for data in a table. For example that a value can't be `null`.

## Database Schema

Database schema is a container of objects which include:
- tables
- views
- stored procedures
- functions

## Data types

[Numeric Data Types](https://mariadb.com/kb/en/data-types-numeric-data-types/)

[String Data Types](https://mariadb.com/kb/en/string-data-types/)

[Date and Time Data Types](https://mariadb.com/kb/en/date-and-time-data-types/)

Also there are some other types at the [Bottom](https://mariadb.com/kb/en/data-types/)

## Command

### Create Database

- To create a new database

  ```
  CREATE DATABASE my_test;
  ```

### Use Database

- To select database

  ```
  USE my_test;
  ```

### Create Table

- First remove the table in case it exists

  ```
  DROP TABLE IF EXISTS Fruits;
  ```

- Create a table

  ```
  CREATE TABLE Fruits (
    ID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(30) NOT NULL,
    DateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ID)
  );
  ```

### Inserting data

Command definition:

  ```
  INSERT INTO <table_name> (column1, column2, ...)
  VALUES (value1, value2, ...)
  ```

Example:

  ```
  INSERT INTO Fruits (Name, DateCreated)
  VALUES ('Apples', '2001-01-01');

  INSERT INTO Fruits (Name)
  VALUES ('Oranges');
  ```
![alt text](/resources/mariadb/db_w_data.png)

### Reading data

Command definition

  ```
  SELECT column1, column2, ...
  FROM <table_name>;
  ```

Examples:

  ```
  SELECT * FROM Fruits;
  ```

  ```
  SELECT ID, Name FROM Fruits WHERE DateCreated > "2000-05-05 16:32:20" LIMIT 2;
  ```

### Updating data

Command definition:

  ```
  UPDATE <table_name>
  SET column1 = value1, column2 = value2, ...
  WHERE condition;

  ```

  > Important is to use the `WHERE` condition, otherwise it will update the values in all the records 

Examples:

  ```
  UPDATE Fruits
  SET Name = 'Mangoes'
  WHERE ID = 2;
  ```

![alt text](/resources/mariadb/db_updated.png)

### Deleting data

Command definition:

  ```
  DELETE FROM <table_name> WHERE condition;
  ```

Example:

  ```
  DELETE FROM Fruits WHERE Name = 'Bananas';
  ```

### Truncating a table

Deleting the data inside a table, but not the table itself.

Command definition:

  ```
  TRUNCATE TABLE <table_name>;
  ```

### Dropping a table

Removes the table completely.

  ```
  DROP TABLE <table_name>;
  ```
