# TODO: Make robust logging + testing
# TODO: Make actual good error system, for now it just quits on errors or exceptions


from databases import ApartmentDatabase
from visit import VisitorManager

def main():
    database = ApartmentDatabase("./data/apt.json")
    results = database.query("obma")

    visitor_manager = VisitorManager(apt_database=database, log_dir="./logs/")

    visitor_manager.sign_in(69, "bruh")
    visitor_manager.sign_out(69, "bruh")

if __name__ == "__main__":
    main()