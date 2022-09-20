DROP VIEW IF EXISTS product_on_discount;
DROP VIEW IF EXISTS products_in_category;

CREATE VIEW product_on_discount AS
SELECT 
  product.id,
  product.name,
  product.price,
  product.url_image as image,
  producer.description,
  ROUND(CAST((product.price - product_discount.discount) AS NUMERIC), 2) as discount,
  product_discount.valid_until,
  address.gps_point AS gpspoint
FROM product
JOIN product_discount
ON product_discount.product_id = product.id
JOIN producer
ON producer.external_id = product.producer_external_id
JOIN producer_address 
ON producer.id = producer_address.producer_id
JOIN address
ON address.id = producer_address.address_id;

CREATE VIEW products_in_category AS 
SELECT product.id,
  product.name,
  product.url_image AS image,
  producer.description,
  product.price,
  category.id AS categoryid,
  category.name AS categoryname,
  address.gps_point AS gpspoint
FROM product
  JOIN product_category ON product.id = product_category.product_id
  JOIN category ON category.id = product_category.category_id
  JOIN producer ON producer.external_id = product.producer_external_id
  JOIN producer_address ON producer.id = producer_address.producer_id
  JOIN address ON address.id = producer_address.address_id;
