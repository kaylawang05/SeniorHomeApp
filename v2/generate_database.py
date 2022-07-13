import datetime
import json
import random

from faker import Faker

from backend import *

def main():
    fake = Faker()

    with open("./database.json", "w") as f:
        apts = []
        
        for i in range(101, 350):
            number = i
            tenants = [fake.name() for _ in range(random.randint(0, 10))]

            visitors = []

            if len(tenants) != 0:
                for _ in range(random.randint(0, 10)):
                    history = []

                    for _ in range(random.randint(1, 5)):
                        begin = datetime.datetime.now() + datetime.timedelta(hours=random.randint(0, 24),minutes=random.randint(0, 60), seconds=random.randint(0, 60))
                        end = begin + datetime.timedelta(hours=random.randint(1, 5))

                        history.append(TimeInterval(begin, end))

                    visitor = Visitor(
                        name = fake.name(),
                        signed_in = True if random.randint(0,1) == 1 else False,
                        history = history,
                    )

                    visitors.append(visitor)

            apt = Apartment(
                number = i,
                tenants = tenants,
                visitors = visitors,
            )

            apts.append(apt)

        f.write(json.dumps(apts, cls=ApartmentEncoder))
        
if __name__ == "__main__":
    main()
