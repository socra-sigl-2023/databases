import csv
from random import randrange, sample, random
from math import sqrt, pi, cos, sin, radians
from weakref import ref
from datetime import datetime, timedelta, timezone
from xmlrpc.client import Boolean

REFERENCE_POSITION = {"lat": 47.781339, "lon": 3.574557} # around Auxerres
RANDOM_POSITION_RADIUS = 250e3 # 250km

def create_discounts(products_csv_path, discount_csv_path):
    with open(discount_csv_path, 'w') as discount_csv:
        discount_writer = csv.writer(discount_csv, delimiter=";")
        discount_writer.writerow([
            "product_id",
            "discount_price",
            "valid_until"
        ])
        with open(products_csv_path, 'r') as product_csv:
            fieldnames = ([
                "external_id",
                "name",
                "url_image",
                "bio",
                "producer_external_id",
                "price"
            ])
            reader = csv.DictReader(product_csv, fieldnames, delimiter=';')
            next(reader, None) # skip header
            product_id = 1
            for row in reader:
                if product_is_on_discount():
                    valid_until = pick_random_validity_date()
                    discount_writer.writerow([
                        product_id,
                        create_discount(row),
                        valid_until.isoformat()
                    ])
                product_id += 1

def create_discount(product) -> float:
    original_price = float(product["price"])
    discount_percentage = randrange(1, 5, 1) * 10
    return round((original_price * discount_percentage) / 100, 2)

def product_is_on_discount() -> Boolean:
    """
        1 out of 5 chance of being on discount
    """
    return randrange(0, 5, 1) == 0

def pick_random_validity_date() -> datetime:
    def create_date(d):
        """
            fmt: "4/1/2022 1:00 AM"
        """
        date_format = '%m/%d/%Y %I:%M %p'
        return datetime.strptime(d, date_format).replace(tzinfo=timezone.utc)
    
    from_date = create_date("4/1/2022 1:00 AM")
    to_date = create_date("12/1/2022 11:59 PM")

    delta = to_date - from_date
    delta_in_seconds = (delta.days * 24 * 60 * 60) + delta.seconds

    random_seconds = randrange(delta_in_seconds)

    return from_date + timedelta(seconds=random_seconds)


if __name__ == '__main__':
    users = create_discounts('scripts/data/product.csv', 'scripts/data/product_discount.csv')
