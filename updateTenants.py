#!/usr/bin/python2
import os
import json
import sys
import getopt
import shutil
from datetime import datetime

aptJsonFile = "apt.json"
#aptJsonFile_tmp = "apt_tmp.json"
update_tenant = False
update_visitor = False
update_car = False

# --------------------------------------------------
# Usage
# --------------------------------------------------
def usage():
    print ("-----------------------------------------------------------------")
    print ("Usage: update.py <options>")
    print ("Options:")
    print ("    -t, --tenant                 Update tenants")
    print ("    -v, --vistor                 Update visitor")
    print ("    -c, --car                    Update visitor's car")
    print ("    -n NUMBER, --number=NUMBER   Specify the APT number")
    print ("    -h, --help                   Show help information and exit")

# --------------------------------------------------
# Take an arg
# --------------------------------------------------
def check_args():

    aptNum = None
    found = 0
    global update_tenant
    global update_visitor
    global update_car

    try:
        opts, args = getopt.getopt(sys.argv[1:], "tvcn:h", ["tenant", "visitor", "number=", "help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-t", "--tenant"):
            update_tenant = True
            update_item = "tenants"
        elif opt in ("-v", "--visitor"):
            update_visitor = True
            update_item = "visitors"
        elif opt in ("-c", "--car"):
            update_car = True
            update_item = "car_plates"
        elif opt in ("-n", "--number"):
            aptNum = arg
        else:
            print ("Unhandled option")
            usage()
            sys.exit(1)

    # Validate aptNum
    if aptNum is None:     # Error #1 - it's empty
        print ("Error: You have to specify an APT number")
        usage()
        sys.exit(2)
    else:                   # Error #2 - it's not an integer
        try:
            int(aptNum)
        except ValueError:
            print ("Error: You have to specify a 3 digit APT number")
            usage()
            sys.exit(2)

        if (int(aptNum) < 100 or int(aptNum) > 350):   # Error #3 - it's not in range
            print ("Error: APT number is not in range")
            usage()
            sys.exit(2)   
    
    # Check to see how many args are true, should be only one
    for item in [update_tenant, update_visitor, update_car]:
        if item:
            found = found + 1
            
    if found is not 1:
        print ("Error: You have to use one of the three options [-t|-v|-c] followed by -n <aptNum>")
        usage()
        sys.exit(2)

    return(update_item, aptNum)

# --------------------------------------------------
# Display the current values for the item to update
# --------------------------------------------------
def display_current(data, update_item, anum):
    for unit in data:
        if unit["aptnum"] == int(anum):
            print ("Here is the current " + update_item + " info for apt " + str(anum))
            print (json.dumps(unit[update_item])) 

# --------------------------------------------------
# Get user's input on what to do (add or delete)
# --------------------------------------------------
def what_to_do(update_item):
    ans = None
    while ans is None:
        ans = raw_input("Do you want to add or delete " + update_item + "? a for add, and d for delete, e to exit: ")
        if ans == "e":
            sys.exit(0)
        elif ans != "a" and ans != "d":
            print ("You have to answer a or d, e to exit: ")
            ans = None
    return ans

# --------------------------------------------------
# Get user's input on what to do (add or delete)
# --------------------------------------------------
def add(data, update_item, anum):
    newitem = raw_input("What is the name of the " + update_item + " do you want to add: ")
    print ("We will add " + newitem)
    for unit in data:
        if unit["aptnum"] == int(anum):
            unit[update_item].append(newitem)
    print ("done")
    return data

# --------------------------------------------------
# Get user's input on what to do (add or delete)
# --------------------------------------------------
def delete(data, update_item, anum):
    for (data_index, unit) in enumerate(data):
        if unit["aptnum"] == int(anum):
            if not unit[update_item]:    # list is empty
                print ("There are no items for " + update_item + " in APT " + anum)
                sys.exit(0)
            else:    
                print ("Which of the following " + update_item + " do you want to delete?")
                index = 1
                for i in unit[update_item]:
                    print (str(index) + ") " + i)
                    index = index + 1
                choice = None
                while choice is None:    
                    choice = raw_input("Enter a number (e to exit): ")
                    if choice == "e":
                        sys.exit(0)
                    elif int(choice) < 1 or int(choice) > index:
                        print ("You have to enter 1-" + index)
                        choice = None
                print ("We will delete " + unit[update_item][int(choice)-1])
                break  # break from the for loop cuz we found the apt
    
    del (data[data_index][update_item][int(choice)-1])
    print ("Done")
    return data

# --------------------------------------------------
# Backup the orig file and copy tmp file to orig
# --------------------------------------------------
def backup_copy():
    backupfile = "./backups/" + aptJsonFile + "." + datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy(aptJsonFile, backupfile)

# --------------------------------------------------
# main()
# --------------------------------------------------
def main():
    # Open the json file and assign it to data
    with open(aptJsonFile) as file:
        data = json.load(file)

    file.close()

    update_item, anum = check_args()

    print ("Checking " + update_item + " at APT number " + anum)
    
    display_current(data, update_item, anum)

    ans = what_to_do(update_item)

    print ("Your answer is " + ans)

    if ans == "a":
        data = add(data, update_item, anum)
    elif ans == "d":
        data = delete(data, update_item, anum)
    else:
        print ("Something is wrong here, existing.")
        sys.exit(3)

    backup_copy()

    # Write data to apt.json
    with open(aptJsonFile, 'w') as file:
        json.dump(data, file)
    
    file.close()
    
    sys.exit(0)

if __name__ == "__main__": main()