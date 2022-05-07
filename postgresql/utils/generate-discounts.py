import csv
from random import randrange, sample, random
from math import sqrt, pi, cos, sin, radians
from weakref import ref

REFERENCE_POSITION = {"lat": 47.781339, "lon": 3.574557} # around Auxerres
RANDOM_POSITION_RADIUS = 250e3 # 250km

def create_discounts(products_csv_path, address_csv_path):
    with open(address_csv_path, 'w') as address_csv:
        address_writer = csv.writer(address_csv, delimiter=";")
        address_writer.writerow([
            "user_id",
            "street",
            "postal_code",
            "gps_point"
        ])
        with open(users_csv_path, 'r') as users_csv:
            fieldnames = (["username"])
            reader = csv.DictReader(users_csv, fieldnames)
            next(reader, None) # skip header
            user_id = 1
            for row in reader:
                random_address = create_user_address(user_id)
                address_writer.writerow([user_id] + random_address)
                user_id += 1
        

if __name__ == '__main__':
    users = create_discounts('data/user.csv', 'data/user_address.csv')
