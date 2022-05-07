/**
 * VIEW that displays products on discount; computing final price directly in the query
 */
CREATE VIEW product_on_discount AS
SELECT 
  product.id,
  product.name,
  product.price,
  product.url_image as image,
  producer.description,
  ROUND(CAST((product.price - product_discount.discount) AS NUMERIC), 2) as discount,
  product_discount.valid_until
FROM product
JOIN product_discount
ON product_discount.product_id = product.id
JOIN producer
ON producer.external_id = product.producer_external_id;

/**
 * Step 5 Challenge
 *
 */
CREATE VIEW products_in_category AS
SELECT 
	product.id,
	product.name,
	product.url_image as image,
	producer.description,
	product.price,
	category.id as categoryId,
	categoryName as categoryName
FROM product 
JOIN product_category
	ON product.id = product_category.product_id
JOIN category
	ON category.id = product_category.category_id
JOIN producer
	ON producer.external_id = product.producer_external_id
WHERE category.id = ${categoryId};