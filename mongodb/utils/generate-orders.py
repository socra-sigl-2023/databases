import csv
from random import randrange, sample, random
from datetime import datetime, timezone, timedelta
from sqlite3 import Timestamp
import pymongo

def write_to_mongo(orders):
    # mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
    db = pymongo.MongoClient('mongodb://sigl2023:sigl2023@localhost:27017')['socrate']
    db.orders.insert_many(orders)


def insert_generated_orders(customer_address_path, product_address_path):
    orders: list = []
    with open(customer_address_path, 'r') as customer_address_csv:
        customer_address = csv.DictReader(
            customer_address_csv, fieldnames=['street','postal_code','gps_point'],
            delimiter=';'
        )
        next(customer_address, None) # skip header
        with open(product_address_path, 'r') as product_address_csv:
            product_address_reader = csv.DictReader(
                product_address_csv,
                fieldnames=['id', 'price', 'gps_point'],
                delimiter=';'
            )
            next(product_address_reader, None) # skip header
            product_address_list = list(product_address_reader)
            customer_id = 1
            for row in customer_address:
                orders_generated = generate_random_product_orders(customer_id, row, product_address_list)
                for order in orders_generated:
                    orders.append(order)
                customer_id += 1
            write_to_mongo(orders)

def generate_random_product_orders(customer_id, a_customer_address, product_address_list: list) -> list[dict]:
    """
        generate a fake set of order by picking products randomly
    """
    number_of_orders = randrange(1, 8, 1)
    def to_gps_position_dict(gps_point):
        [lon, lat] = str.split(gps_point, ',')   
        return dict(lat=lat,lon=lon)

    customer_orders: list = []
    for i in range(number_of_orders):
        number_of_products = randrange(1, 4, 1)
        sample_product_indexes = sample(range(0, len(product_address_list)), k=number_of_products)
        sample_products = []
        for idx in sample_product_indexes:
            sample_products.append(product_address_list[idx])
        order_price = 0
        basket = []
        for p in sample_products:
            basket.append(dict(
                product_id=p['id'],
                producer_gps_position=to_gps_position_dict(p['gps_point']),
                quatity=1000)
            )
            order_price += float(p['price'])
        (created_at, delivered_at) = pick_random_dates()
        user_geo_point = to_gps_position_dict(a_customer_address['gps_point'])
        order_price_rounded = round(order_price, 2)
        new_order = dict(
                customer_id= customer_id,
                created_at= created_at,
                user_geo_point= user_geo_point,
                products_ordered= basket,
                order_price= order_price_rounded,
                status= 'delivered',
                delivered_at= delivered_at)
        customer_orders.append(new_order)
    return customer_orders
        

        

def pick_random_dates() -> tuple[int, int]:
    def create_date(d: datetime):
        """
            fmt: "4/1/2022 1:00 AM"
        """
        date_format = '%m/%d/%Y %I:%M %p'
        return datetime.strptime(d, date_format).replace(tzinfo=timezone.utc)
    
    def to_timestamp(d: datetime) -> int:
        return int(d.timestamp() * 1000)

    from_date = create_date("6/1/2021 1:00 AM")
    to_date = create_date("5/1/2022 11:59 PM")

    delta = to_date - from_date
    delta_in_seconds = (delta.days * 24 * 60 * 60) + delta.seconds

    random_seconds = randrange(delta_in_seconds)

    random_date = from_date + timedelta(seconds=random_seconds)
    random_date_plus_three_days = random_date + timedelta(days=3)
    return (to_timestamp(random_date), to_timestamp(random_date_plus_three_days))

if __name__ == '__main__':
    """
        Product addresses comes with:
        SELECT
        	product.id,
        	address.gps_point
        FROM product
        JOIN producer
        	ON producer.external_id = product.producer_external_id
        JOIN producer_address
        	ON producer_address.producer_id = producer.id
        JOIN address
        	ON address.id = producer_address.address_id;
    """
    comments_base = insert_generated_orders(
        'postgresql/scripts/data/customer_address.csv',
        'mongodb/scripts/data/product_address.csv'
    )
    
