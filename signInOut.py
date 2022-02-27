#!/usr/bin/python2
import os
import json
import sys
import getopt
import shutil
from datetime import datetime

aptJsonFile = "apt.json"
today = datetime.now().strftime("%Y%m%d")
todayslog = "logs/" + today
todays_tmp_log = "logs/tmp_" + today

# --------------------------------------------------
# Get user's input on what to do (sign in or out)
# --------------------------------------------------
def what_to_do():
    ans = None
    while ans is None:
        ans = raw_input("Are you signing in or signing out? (i for signin, o for sign out, e for exit): ")
        if ans == "e":
            sys.exit(0)
        elif ans != "i" and ans != "o":
            print ("You have to answer i or o, e to exit: ")
            ans = None
    return ans

# --------------------------------------------------
def get_apt():
    aptnum = None
    while aptnum is None:    
        aptnum = raw_input("Enter APT number, e.g. 305 (e to exit): ")
        if aptnum == "e":
            sys.exit(0)
        else:
            try:
                int(aptnum)         # Is it an integer
                if (int(aptnum) < 100 or int(aptnum) > 350):   # it's not in range
                    print ("Error: APT number is not in range, please enter (101-348):")
                    aptnum = None
            except ValueError:
                print ("Error: You have to specify a 3 digit APT number")
                aptnum = None
    return aptnum
            
# --------------------------------------------------
def get_visitors(aptnum):
    visitors = []
    choice = None
    found = 0
    with open(aptJsonFile) as file:
        data = json.load(file)

    for unit in data:
        if unit["aptnum"] == int(aptnum):
            found = 1
            break

    if found == 0:
        print ("Can not find this apartment, something is worng.")
        return visitors

    if not unit["visitors"]: 
        print ("There are no visitors registered for APT " + aptnum + ", please go back to the main menu and add the visitors.")
        return visitors
        
    print ("Here are the visitors registered for APT " + str(aptnum) + ":")
    print ("If the visitor is not on the list, please enter e to go back to the main menu to update the visitors.")
    for i, v in enumerate(unit["visitors"]):
        index = i+1
        print (" " + str(index) + ") " + v)

    while choice is None:
        choice = raw_input("Enter the number of the visitor you are signing in, e.g. 1 or 1,2 (a for all, e to exit): ")
        if choice == "e":
            sys.exit(0)

        if choice == "a":
            visitors = unit["visitors"]
            return visitors

        if ("," in choice):
            list = choice.split(",")
            for v in list:
                try:
                    int(v)
                    visitors.append(unit["visitors"][int(v)-1])
                except ValueError:
                    print ("You have to enter a numbers 1 - " + str(index) + ", seperated by ,")
                    choice = None
        else:
            try:
                int(choice)
                if (int(choice) < 1 or int(choice) > index):
                    print ("You choice has to be between 1 - " + str(index))
                    choice = None
                else:
                    visitors.append(unit["visitors"][int(choice)-1])
            except ValueError:
                print ("You have to enter a number 1 - " + str(index))
                choice = None
    return visitors

# --------------------------------------------------
def sign_in_to_file (aptnum, visitors):
    current_time = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%Y%m%d")
    todayslog = "logs/" + today
    file = open(todayslog, 'a')
    print ("You are singing in at " + current_time + " for:")
    for v in visitors:
        file.write(str(aptnum) + "," + v + "," + str(current_time) + ",\n")
        print (v)
    file.close()

# --------------------------------------------------
def sign_out_to_file (aptnum):
    found = 0
    current_time = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%Y%m%d")
    todayslog = "logs/" + today
    todays_tmp_log = "logs/tmp_" + today
    file = open(todayslog, 'r')
    tmpfile = open(todays_tmp_log, 'w')
    for line in file:
        line = line.rstrip('\n')
        items = line.split(",")
        # Only write the sign out time if aptnum is found and last item is empty (no signout time)
        if items[0] ==  str(aptnum) and not items[3]: # last item is empty (signout is empty)
            print ("Found")
            found = found + 1
            tmpfile.write(line + current_time + '\n')
        else:
            tmpfile.write(line + '\n')        

    tmpfile.close()
    file.close()
    shutil.copy(todays_tmp_log, todayslog)
    os.remove(todays_tmp_log)
    
    if found == 0:
        print ("We are unable to find your sign in time.")
    else:
        print ("You are successfully singed out at " + current_time)
    
# --------------------------------------------------
def signin():
    aptnum = get_apt()
    print ("Apt number is " + aptnum)
    visitors = get_visitors(aptnum)
    print ("Here are the visitors " + str(visitors))
    sign_in_to_file (aptnum, visitors)

# --------------------------------------------------
def signout():
    aptnum = get_apt()
    print ("Apt number is " + aptnum)
    sign_out_to_file (aptnum)

# --------------------------------------------------
# main()
# --------------------------------------------------
def main():
    ans = what_to_do()

    print ("Your answer is " + ans)

    if ans == "i":
        signin()
    elif ans == "o":
        signout()
    elif ans == "e":
        sys.exit(0)
    else:
        print ("Something is wrong here, existing.")
        sys.exit(3)

if __name__ == "__main__": main()