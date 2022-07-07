from backend import *

def main():
    apts = ApartmentDatabase("./data/apt.json")

    apt_102 = apts.get_apt(102).unwrap()

    print(apt_102.number)

    print(apt_102)

    apts.save()

if __name__ == "__main__":
    main()