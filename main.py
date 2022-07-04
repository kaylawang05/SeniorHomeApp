# TODO: Make robust logging + testing
# TODO: Make actual good error system, for now it just quits on errors or exceptions

from databases import ApartmentDatabase
from visit import VisitorManager

def main():
    database = ApartmentDatabase("./data/apt.json")

    print(database.rows)

    print()

    print(database.get_apt(2))

    print()

    results = database.query("da")

    for result in results:
        print(result)

    print()

    print(database.remove_visitor(69, "bruh"))

    print(database.get_apt(69))

    print()

    database.save()


    # results = database.query("10")

    # visitor_manager = VisitorManager(apt_database=database, log_dir="./visitor-logs/")

    # visitor_manager.sign_in(69, "david")
    # visitor_manager.sign_out(69, "david")
    
if __name__ == "__main__":
    main()