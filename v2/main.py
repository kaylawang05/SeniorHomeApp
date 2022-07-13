from backend import *

def main():
    apts = ApartmentManager(db_path="./database.json", log_dir="./visitor-logs/")

    try:
        apt = apts.get_apt(102)
    except ApartmentNotFound:
        print("oh no, apartment not found")
    
    apts.sign_in("Teresa Woods", 101)
    apts.sign_out("Teresa Woods", 101)

if __name__ == "__main__":
    main()