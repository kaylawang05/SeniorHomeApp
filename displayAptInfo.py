#!/usr/bin/python2
import os
import json
import sys
import getopt
import shutil
from datetime import datetime

aptJsonFile = "apt.json"
aptJsonFile_tmp = "apt_tmp.json"
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
            
    if found != 1:
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
            print ("In display: " + json.dumps(unit[update_item])) 
#    tkinterstring = f'{json.dumps(unit[update_item])}'
            return json.dumps(unit[update_item])
    #return tkinterstring

# --------------------------------------------------
# main()
# --------------------------------------------------
def main():
    # Open the json file and assign it to data
    with open(aptJsonFile) as file:
        data = json.load(file)

    update_item, anum = check_args()
    
    display_current(data, update_item, anum)

    sys.exit(0)

if __name__ == "__main__": main()