import json
import sys

aList = []
aNumbers = [
    101, 102, 103, 104, 105,
    201, 202, 203, 204, 205,
    301, 302, 303, 304, 305
]
aptJsonFile = "apt.json"

for n in aNumbers:
    thisUnit = {
        "AptNum": n,
        "Tenants": [],
        "Visitors": [],
        "VisitorsCars": []
    }
    aList.append(thisUnit)

jsonStr = json.dumps(aList)

f = open(aptJsonFile, "w")
f.write(jsonStr)
# print(jsonStr)
f.close()
sys.exit(0)

aNum = input("What aprtment are you visiting? Enter apt number (e.g. 216): ")
print("You entered: " + str(aNum))

while aNum not in aNumbers:
    aNum = raw_input(str(aNum) + " is not a valid apartment number, please try again or enter e to exit: ")
    if aNum == "e":
        print("Good Bye...")
        sys.exit(0)

print("Here is the info for apt " + str(aNum) + ":")
for unit in aList:
    if unit["AptNum"] == aNum:
        print(unit)

ans = raw_input("Do you want to edit the info? Enter y for yes, and n for no: ")
