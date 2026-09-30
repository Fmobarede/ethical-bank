CREATE TABLE employees (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50),
    salary NUMBER
);

INSERT INTO employees VALUES (1, 'Alice', 50000);
INSERT INTO employees VALUES (2, 'Bob', 62000);
COMMIT;

SELECT * FROM employees;

INSERT INTO employees VALUES (1, 'Alice', 50000);
INSERT INTO employees VALUES (2, 'Bob', 62000);
COMMIT;



INSERT INTO employees VALUES (1, 'Alice', 50000);

INSERT INTO employees VALUES (2, 'Bob', 62000);
SELECT * FROM employees;

UPDATE employees
SET salary = 54000
WHERE name = 'Alice';
SELECT * FROM employees;
DELETE FROM employees
WHERE name = 'Bob';
COMMIT;
SELECT * FROM employees;

CREATE TABLE departments (
    dept_id NUMBER PRIMARY KEY,
    dept_name VARCHAR2(50)
);

INSERT INTO departments VALUES (1, 'HR');
INSERT INTO departments VALUES (2, 'IT');

COMMIT;

ALTER TABLE employees
ADD dept_id NUMBER;

UPDATE employees SET dept_id = 1 WHERE name = 'Alice';
COMMIT;

SELECT * FROM employees;

SELECT
    e.name,
    e.salary,
    d.dept_name
FROM employees e
JOIN departments d
ON e.dept_id = d.dept_id;

SELECT * FROM employees;
SELECT * FROM departments;
INSERT INTO departments VALUES (1, 'HR');
SELECT * FROM departments;


SELECT
    e.name,
    e.salary,
    d.dept_name
FROM employees e
JOIN departments d
ON e.dept_id = d.dept_id;

SELECT
    d.dept_name,
    COUNT(e.id) AS total_employees
FROM employees e
JOIN departments d
ON e.dept_id = d.dept_id
GROUP BY d.dept_name;
COMMIT;