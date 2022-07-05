from returns.result import Result, Failure, Success

from apartment import ApartmentDatabase, Error
from visit import VisitorManager

def main():
    database = ApartmentDatabase("./data/apt.json")

    print(database.rows)

    print()

    print(database.get_apt(2))

    print()

    results = database.query("le")

    for result in results:
        print(result)

    print()

    print(database.remove_visitor(69, "bruh"))

    print()

    print(database.get_apt(69))

    print()

    database.save()

    visitor_manager = VisitorManager(database, "./visitor-logs/")

    print(visitor_manager.sign_in(69, "bruh"))

    print()

    print(visitor_manager.visitors)

    print()

    print(visitor_manager.sign_out(69, "bruh"))
    
    print()

    print(visitor_manager.visitors)

    print()

if __name__ == "__main__":
    main()