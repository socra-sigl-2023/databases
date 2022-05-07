DROP TABLE IF EXISTS producer CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS product_discount CASCADE;
DROP TABLE IF EXISTS customer_address CASCADE;
DROP TABLE IF EXISTS producer_address CASCADE;
DROP TABLE IF EXISTS address CASCADE;
DROP TABLE IF EXISTS customer CASCADE;

CREATE TABLE producer (
    id SERIAL PRIMARY KEY,
    external_id INT NOT NULL,
    name TEXT,
    description TEXT
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    external_id INT NOT NULL,
    name TEXT,
    url_image TEXT,
    bio TEXT,
    producer_external_id INT NOT NULL,
    price NUMERIC
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    street TEXT,
    postal_code TEXT,
    gps_point POINT
);

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    username TEXT
);

/* 
 *  Relation tables
**/
CREATE TABLE product_discount (
    product_id INT REFERENCES product(id) ON DELETE NO ACTION,
    discount FLOAT,
    active_until DATE
);

CREATE TABLE customer_address(
    customer_id INT REFERENCES customer(id) ON DELETE NO ACTION,
    address_id INT REFERENCES address(id) ON DELETE NO ACTION
);

CREATE TABLE producer_address(
    address_id INT REFERENCES address(id) ON DELETE NO ACTION,
    producer_id INT REFERENCES producer(id) ON DELETE NO ACTION
);
