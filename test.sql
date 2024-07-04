-- DROP TABLE person;

-- CREATE TABLE person (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     firstname VARCHAR(50) NOT NULL,
--     lastname VARCHAR(50) NOT NULL,
--     age INTEGER,
--     accountbalance REAL
-- );

-- DROP TABLE product;

-- CREATE TABLE product (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     productname VARCHAR(50) NOT NULL,
--     description VARCHAR(250) NOT NULL,
--     quantityinstock INTEGER,
--     price REAL
-- );

-- DROP TABLE orders;

-- CREATE TABLE orders (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     transaction_date DATE NOT NULL,
--     person_id INTEGER NOT NULL,
--     product_id INTEGER NOT NULL,
--     quantity INTEGER NOT NULL,
--     total_cost REAL NOT NULL,
--     FOREIGN KEY (person_id) REFERENCES person(id),
--     FOREIGN KEY (product_id) REFERENCES product(id)
-- );



-- INSERT INTO person (firstname, lastname, age, accountbalance) VALUES ('Fred', 'Garvin', 52, 1102.35);
-- SELECT * FROM person;
-- INSERT INTO product (productname, description, quantityinstock, price) VALUES ('Black Diamond', 'A diamonad that is black', 125, 50.99);
-- SELECT * FROM product;

DELETE FROM person WHERE id=18;



