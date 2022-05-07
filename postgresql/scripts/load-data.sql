COPY producer(external_id,name,description)
FROM '/tmp/scripts/data/producer.csv' WITH DELIMITER ';' CSV HEADER;

COPY product(external_id,name,url_image,bio,producer_external_id,price)
FROM '/tmp/scripts/data/product.csv' DELIMITER ';' CSV HEADER;

COPY category(name)
FROM '/tmp/scripts/data/category.csv' DELIMITER ';' CSV HEADER;

COPY customer(username)
FROM '/tmp/scripts/data/customer.csv' DELIMITER ';' CSV HEADER;

COPY address(street,postal_code,gps_point)
FROM '/tmp/scripts/data/customer_address.csv' DELIMITER ';' CSV HEADER;

COPY address(gps_point,street,postal_code)
FROM '/tmp/scripts/data/address_from_producer.csv' DELIMITER ';' CSV HEADER;

COPY customer_address(customer_id, address_id)
FROM '/tmp/scripts/data/customer_id_address_id.csv' DELIMITER ';' CSV HEADER;

COPY producer_address(address_id, producer_id)
FROM '/tmp/scripts/data/producer_address.csv' DELIMITER ';' CSV HEADER;
