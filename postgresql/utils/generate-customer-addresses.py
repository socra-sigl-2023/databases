import csv
from random import randrange, sample, random
from math import sqrt, pi, cos, sin, radians
from weakref import ref

REFERENCE_POSITION = {"lat": 47.781339, "lon": 3.574557} # around Auxerres
RANDOM_POSITION_RADIUS = 250e3 # 250km

def create_user_addresses(users_csv_path, address_csv_path, user_id_address_id_path):
    with open(address_csv_path, 'w') as address_csv:
        address_writer = csv.writer(address_csv, delimiter=";")
        address_writer.writerow([
            "street",
            "postal_code",
            "gps_point"
        ])
        with open(user_id_address_id_path, 'w') as user_id_address_id_csv:
            user_id_address_id_writer = csv.writer(user_id_address_id_csv, delimiter=";")
            user_id_address_id_writer.writerow([
                "customer_id",
                "address_id"
            ])
            with open(users_csv_path, 'r') as users_csv:
                fieldnames = (["username"])
                reader = csv.DictReader(users_csv, fieldnames)
                next(reader, None) # skip header
                cpt = 1
                for row in reader:
                    random_address = create_user_address(cpt)
                    address_writer.writerow(random_address)
                    user_id_address_id_writer.writerow([cpt, cpt])
                    cpt += 1
            

def random_location():
    """
        pick a random geo position (lat, lon) within a RANDOM_POSITION_RADIUS
        from the REFERENCE_POSITION.

        Returns a tuple (lat, lon)

        See. https://gis.stackexchange.com/questions/25877/generating-random-locations-nearby
    """
    radius_in_degrees = RANDOM_POSITION_RADIUS / 111000
    x0 = REFERENCE_POSITION["lon"]
    y0 = REFERENCE_POSITION["lat"]

    u = random()
    v = random()

    w = radius_in_degrees * sqrt(u)
    t = 2 * pi * v
    x = w * cos(t)
    y = w * sin(t)

    new_x = x / cos(radians(y0))
    
    lon = round(new_x + x0, 6)
    lat = round(y + y0, 6)

    return (lat, lon)

def create_user_address(user_id):
    (lat, lon) = random_location()
    return [
        f"{user_id}, User {user_id}'s street",
        f"{10000 + (user_id % 84000)}",
        f"{lat},{lon}"
    ]

if __name__ == '__main__':
    create_user_addresses('data/customer.csv', 'data/customer_address.csv', 'data/customer_id_address_id.csv')
