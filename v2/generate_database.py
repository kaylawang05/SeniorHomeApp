import json
import random

from faker import Faker

from backend import *
from backend.apartment import ApartmentEncoder

fake = Faker()

with open("./data/apts.json", "w") as f:
    apts = []
    
    for i in range(101, 350):
        number = i
        tenants = [fake.name() for _ in range(random.randint(0, 10))]
        visitors = visitors = [fake.name() for _ in range(random.randint(0, 10))] if len(tenants) != 0 else []

        apt = Apartment(
            number = i,
            tenants = tenants,
            visitors = visitors,
        )

        apts.append(apt)

    f.write(json.dumps(apts, cls=ApartmentEncoder))
