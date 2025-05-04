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

### List all databases

```
SHOW DATABASES;
```

### Use the database

```
USE my_test;
```

### List all tables in a database

```
SHOW TABLES;
```

### Create Database

```
CREATE DATABASE IF NOT EXISTS my_test;
```

### Create Table

- First remove the table in case it exists

  ```
  DROP TABLE IF EXISTS Fruits;
  ```

- Create a table

  ```
  CREATE TABLE IF NOT EXISTS Fruits (
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

Command definition:

  ```
  DROP TABLE <table_name>;
  ```

### Removing duplicates from query result

Display only records that are unique.

Command definition:

  ```
  SELECT DISTINCT column1, column2
  FROM <table_name>;
  ```

Example:

Given we have a table which has inventory of films that have multiple copies, when we want to display only unique values:

  ```
  SELECT DISTINCT film_id FROM inventory; 
  ```

### Sorting data from the query

Query by default returns the data in the order how the data was entered into the table.

Command definition:

  ```
  SELECT column1, column2, ...
  FROM 
  ORDER BY column1, ... ASC/DESC
  ```

  > Note the default is ASC

Example

  ```
  SELECT first_name, last_name
  FROM customer
  ORDER BY last_name DESC;
  ```

### Aliases

Aliases are used to give a table or column in a table a temporary name. It has lifetime of the query. Aliases are used to make column names more readabe. They make writing queries shorter and thus more efficient.

Command definitions:

- column alias

  ```
  SELECT column_name AS alias_name_1 FROM table_1;
  ```
- table alias

  ```
  SELECT column_name(s) FROM table_1 AS t1;
  ```
  
  > NOTE: the `AS` is not necessary, we can use just space ` `

Examples:

  ```
  SELECT customer_id as ID, last_name AS lname FROM customer;
  ```
![alt text](/resources/mariadb/column_alias.png)

  ```
  SELECT c.customer_id, c.last_name FROM customer AS c;
  ```

  > NOTE: this is useful when doing for example table joins

### Aggregate functions

#### Average

Calculate the average value of a numeric column

Command definition:

  ```
  SELECT AVG (column)
  FROM <table_name>;
  ```

Example:

  ```
  SELECT AVG (replacement_cost)
  FROM film;
  ```

#### Count

The `SELECT COUNT` function in SQL is used to count rows in a table or count non-null values in a specific column. It's commonly used for summarizing data and checking the number of records that meet certain conditions.

Command definition:

  ```
  SELECT COUNT (column) / (*)
  FROM <table_name>;
  ```

> NOTE: `*` takes into account the whole record

Examples:

  ```
  SELECT COUNT(*) FROM employees;
  ```

  - Returns the total number of rows in the employees table.

  ```
  SELECT COUNT(email) FROM users;
  ```

  - Returns the number of users who have an email recorded (ignores NULL values).

#### Maximum value

Return maximum value in a set of values

Command definition:

  ```
  SELECT MAX (column)
  FROM <table_name>;
  ```

Example:

  ```
  SELECT MAX (replacement_cost)
  FROM film;
  ```

#### Minimum value

Return minimum value in a set of values

Command definition:

  ```
  SELECT MIN (column)
  FROM <table_name>;
  ```

Example:

  ```
  SELECT MIN (replacement_cost)
  FROM film;
  ```

#### Sum

Return a sum of values

Command definition:

  ```
  SELECT SUM (column)
  FROM <table_name>;
  ```

Example:

  ```
  SELECT SUM (rental_duration)
  FROM film;
  ```

#### Group by

The `GROUP BY` clause in SQL is used to group rows that have the same values in specified columns and apply aggregate functions like COUNT, SUM, AVG, MIN, or MAX to each group.

- The query groups rows by a specified column.

- It applies aggregate functions to those groups.

- The result displays one row per unique group.

Command definition:

  ```
  SELECT column_name(s)
  FROM table_name
  WHERE condition
  GROUP BY column_name(s)
  ORDER BY column_name(s);
  ```

Example:

![alt text](/resources/mariadb/group_by_source.png)

  ```
  SELECT department, COUNT(*) AS employee_count
  FROM employees
  GROUP BY department;
  ```

![alt text](/resources/mariadb/group_by_result.png)

- The query groups employees by department and shows how many employees are in each department.

#### Having

The `HAVING` clause in SQL is used to filter results after the `GROUP BY` operation. Unlike WHERE, which filters individual rows, HAVING filters grouped records based on aggregate functions like COUNT, SUM, AVG, MAX, or MIN.

![alt text](/resources/mariadb/having.png)

Command definition:

  ```
  SELECT column_name(s)
  FROM table_name
  GROUP BY column_name(s)
  HAVING condition..
  ORDER BY column_name(s);
  ```

Example:

![alt text](/resources/mariadb/having_source.png)

  ```
  SELECT department, COUNT(*) AS employee_count
  FROM employees
  GROUP BY department
  HAVING COUNT(*) > 2;
  ```

![alt text](/resources/mariadb/having_result.png)

- This filters out departments that have 2 or fewer employees and keeps only HR, which has more than 2.

### Table Joins - Extracting data from multiple tables

A `JOIN` combines columns from two or more tables into a single set.

Basic Join Syntax:

  ```
  SELECT column_name(s)
  FROM table1
  X JOIN table2 ON table1.column_name = table2.column_name;
  ```

> NOTE: The `X` above is the type of `JOIN`. The `ON` is the condition.


#### Inner Join

Returns records that have matching values in both tables. So participating tables need to have columns that match. If there is no match, the row is excluded from the result.

- Compares rows in both tables using a specified column.

- Returns only rows where there is a match in both tables.

- If a record exists in one table but not in the other, it is not included in the result.

Command definition:

  ```
  SELECT column_name(s)
  FROM table1
  INNER JOIN table2 ON table1.column_name = table2.column_name;
  ```
Example:

Given we have two tables which have a common column `customer_id`:

![alt text](/resources/mariadb/inner_join_source.png)

  ```
  SELECT customers.name, orders.product
  FROM customers
  INNER JOIN orders ON customers.id = orders.customer_id;
  ```

Result:

![alt text](/resources/mariadb/inner_join_result.png)

#### Cross Join

Join of every row of one table to every row of another table. This is also called a cartesian product. Any `JOIN` without a `ON` clause is a `CROSS JOIN`. Tables do not have to have matching columns. TLDR it creates all the possible combinations.

- If one table has N rows and the other has M rows, the result will contain N × M rows.

- The final result includes every combination of records from both tables.

Command definition:

  ```
  SELECT *
  FROM table1
  CROSS JOIN table2;
  ```
> NOTE: The `CROSS` here is not required

Example:

Given we have two tables, `colors` has 3 records, `shapes` has 2 records

![alt text](/resources/mariadb/cross_join_source.png)

  ```
  SELECT colors.color, shapes.shape
  FROM colors
  CROSS JOIN shapes;
  ```

Result:

We get 6 records (3x2) of all colors for each shape.

![alt text](/resources/mariadb/cross_join_result.png)

#### Left Join

Return all records from the left table, and the matched records from the right table. Retrieves all rows from the left table, even if there is no matching row in the right table. If there's no match, NULL values are returned for the right table’s columns.

- The query starts with all rows from the left table.

- It checks for matching rows in the right table using a specified condition.

- If there is no match, NULL values are returned for the columns from the right table.

Command definition:

  ```
  SELECT column_name(s)
  FROM table1
  LEFT JOIN table2 ON table1.column_name = table2.column_name;
  ```
Example:

Given we have two tables which have matching `id` and `customer_id` columns

![alt text](/resources/mariadb/left_join_source.png)

  ```
  SELECT customers.name, orders.product
  FROM customers
  LEFT JOIN orders ON customers.id = orders.customer_id;
  ```

Result:

![alt text](/resources/mariadb/left_join_result.png)

- Charlie is included even though he has no order, with `NULL` in the `product` column.

#### Right Join

Return all records from the right table, and the matched records from the left table. Retrieves all rows from the right table, even if there is no matching row in the left table. If there's no match, NULL values are returned for the left table’s columns.

- Starts with all rows from the right table.

- Checks for matches in the left table based on a condition.

- If a match exists, the row is combined.

- If no match exists, `NULL` values appear for the left table’s columns.

Command definition:

  ```
  SELECT column_name(s)
  FROM table1
  RIGHT JOIN table2 ON table1.column_name = table2.column_name;
  ```

Example:

Given we have two tables which have matching `id` and `customer_id` columns

![alt text](/resources/mariadb/right_join_source.png)

  ```
  SELECT customers.name, orders.product
  FROM customers
  RIGHT JOIN orders ON customers.id = orders.customer_id;
  ```

Result:

![alt text](/resources/mariadb/right_join_result.png)

- The Tablet order remains, but since there’s no matching customer, NULL appears under the name column.

### Union operator

Used to combine the result-set of two or more SELECT statements into a single result set. Each SELECT statement within UNION must have the same number of columns. The columns must also have similar or convertible data types. The columns in each SELECT statement must also be in the same order. Columns names from the first SELECT statement are used as the column names for the results returned.

Union can be used with `DISTINCT` (this is default if omitted) and `ALL` keyword. The `DISTINCT` causes duplicate rows to be removed from the results.

Command definition:

  ```
  SELECT column1, column2
  FROM table1
  UNION DISTINCT/ALL
  SELECT column1, column2
  FROM table2;
  ```

Example:

![alt text](/resources/mariadb/union_source.png)

  ```
  SELECT name, city FROM customers
  UNION DISTINCT
  SELECT name, city FROM suppliers;
  ```

![alt text](/resources/mariadb/union_result.png)

- Charlie (Hamburg) appears only once, since it's exactly the same in both tables.

- David appears twice, because he is listed in two different cities (Frankfurt and Cologne), meaning those rows are not duplicates.

### Except operator

Used to combine the result-set of two or more SELECT statements into a single result set. Returns rows in first query not present in output of second query. Returns distinct rows from the first query not in output of second query. The columns in each SELECT statement must also be in the same order. The columns must also have similar or convertible data types.

Command definition:

  ```
  SELECT column1, column2
  FROM table1
  EXCEPT
  SELECT column1, column2
  FROM table2;
  ```

Example:

![alt text](/resources/mariadb/union_source.png)

  ```
  SELECT name, city FROM customers
  EXCEPT
  SELECT name, city FROM suppliers;
  ```

![alt text](/resources/mariadb/except_result.png)

- The query starts with all rows from the customers table.

- It then removes any row that exactly matches a row from the suppliers table.

- Since Charlie | Hamburg is present in both tables, it gets excluded.

- However, David | Frankfurt remains because his entry in suppliers is David | Cologne—a different city.

### Intersect operator

Used to combine the result-set of two or more SELECT statements into a single result set. Returns all rows in both result sets. The columns must also have similar or convertible data types.

Command definition:

  ```
  SELECT column1, column2
  FROM table1
  INTERSECT
  SELECT column1, column2
  FROM table2;
  ```

Example:

![alt text](/resources/mariadb/union_source.png)

  ```
  SELECT name, city FROM customers
  INTERSECT
  SELECT name, city FROM suppliers;
  ```

![alt text](/resources/mariadb/intersect_result.png)

- "Charlie | Hamburg" appears in both customers and suppliers, so it's included.

- "David | Frankfurt" is not included because "David | Cologne" exists in suppliers, which is a different city.

- "Alice", "Bob", "Eve", and "Frank" do not exist in both tables, so they are excluded.

### Comparison operators

![alt text](/resources/mariadb/comparison_operators.png)

### AND OR operators

![alt text](/resources/mariadb/and_or_operators.png)