CREATE OR REPLACE FUNCTION random_price(low INT ,high INT) 
   RETURNS FLOAT AS
$$
BEGIN
    RETURN random() * (high - low + 1) + low;
END;
$$ language 'plpgsql' STRICT;

CREATE OR REPLACE FUNCTION random_price_for(category TEXT)
    RETURNS FLOAT AS
$$
BEGIN
    CASE
        WHEN category LIKE '%Vin%' THEN RETURN random_price(5, 35);
        WHEN category LIKE '%Fromages%' THEN RETURN random_price(4, 13);
        WHEN category = 'Viandes et salaisons' THEN RETURN random_price(8, 25);
        WHEN category = 'Epicerie sucrée' THEN RETURN random_price(1, 4);
        WHEN category = 'Bois' THEN RETURN random_price(1, 10);
        WHEN category = 'Autres boissons alcoolisées' THEN RETURN random_price(10, 30);
        WHEN category = 'Epicerie salée' THEN RETURN random_price(3, 7);
        WHEN category = 'Légumes frais' THEN RETURN random_price(2, 6);
        WHEN category = 'Plats cuisinés et conserves' THEN RETURN random_price(4, 14);
        WHEN category = 'Produits Bien être' THEN RETURN random_price(5, 15);
        WHEN category = 'Boissons non alcoolisées' THEN RETURN random_price(1, 5);
        WHEN category = 'Horticulture' THEN RETURN random_price(1, 10);
        WHEN category = 'Fruits frais' THEN RETURN random_price(2, 6);
        WHEN category = 'Produits de la mer frais' THEN RETURN random_price(15, 30);
        ELSE RETURN random_price(1, 5);
    END CASE;
END;
$$ language 'plpgsql' STRICT;

COPY (SELECT DISTINCT (entreprise_id) as external_id, entreprise_nom as name, entreprise_descr_fr as description from "produit-sud-de-france" WHERE coordonnees_gps is not null)
TO '/tmp/producer.csv' DELIMITER ';' CSV HEADER;

COPY (SELECT DISTINCT (entreprise_id) as external_id, coordonnees_gps as gps_point, entreprise_adresse as street, entreprise_code_postal as postal_code from "produit-sud-de-france" WHERE coordonnees_gps is not null)
TO '/tmp/address_from_producer_eid.csv' DELIMITER ';' CSV HEADER;

COPY (SELECT produit_id as external_id, produit_nom as name, url_image, produit_bio as bio, entreprise_id as producer_external_id, ROUND(CAST(random_price_for(produit_categorie1) AS NUMERIC),2) as price from "produit-sud-de-france")
TO '/tmp/product.csv' DELIMITER ';' CSV HEADER;

COPY(SELECT DISTINCT produit_categorie1 as name from "produit-sud-de-france")
TO '/tmp/category.csv' DELIMITER ';' CSV HEADER;