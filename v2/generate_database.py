import json
import random

from faker import Faker

from backend import *

def main():
    fake = Faker()

    with open("./data/apts.json", "w") as f:
        apts = []
        
        for i in range(101, 350):
            tenants = [fake.name() for _ in range(random.randint(0, 2))]
            visitors = [fake.name() for _ in range(random.randint(0, 10))] if len(tenants) != 0 else []
            
            apt = Apartment(
                number = i,
                tenants = tenants,
                visitors = visitors,
            )

            apts.append(apt)

        f.write(json.dumps(apts, cls=ApartmentEncoder))
        
if __name__ == "__main__":
    main()
