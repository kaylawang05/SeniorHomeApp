from cgitb import text
import json
from tkinter import *
#from tkinter import ttk
from displayAptInfo import display_current
from signInOut import sign_in_to_file
from signInOut import sign_out_to_file

root = Tk()
root.title('Springfield Senior Home')
root.geometry("1200x800")

#---------------------------------------------------------------------------------------------
# Get the apartment list from the apt.json
#---------------------------------------------------------------------------------------------
aptJsonFile="./apt.json"
with open(aptJsonFile) as file:
    data = json.load(file)

def getApt():
    aptnums = []
    for unit in data:
        aptnums.append(unit["aptnum"])
    return aptnums

aptlist = getApt()

#---------------------------------------------------------------------------------------------
# The title 
#---------------------------------------------------------------------------------------------
title = Label(root, text="SignIn and SignOut", font=("Helvetica", 20))
title.pack(side=TOP, pady=50)

#---------------------------------------------------------------------------------------------
# The frame for the list boxes
#---------------------------------------------------------------------------------------------
frame2 = Frame(root)
frame2.pack(pady=20)

l1lab = Label(frame2, text="Apt Numbers", justify=LEFT, font=("Helvetica", 14))
l1lab.grid(row=1, column=0, sticky="w", padx=5)
l2lab = Label(frame2, text="Visitors", justify=LEFT, font=("Helvetica", 14))
l2lab.grid(row=1, column=1, sticky= "w", padx=25)

list1 = Listbox(frame2)
list2 = Listbox(frame2)
list1.grid(row=2, column=0, sticky="w")
list2.grid(row=2, column=1, padx=20, sticky="w")

user_select = { "apt": "", "visitors": ""}

def item2_picked(e):
    user_select["visitors"] = list2.get(ANCHOR) 

def item1_picked(e):
    list2.delete('0', 'end')
    user_select["apt"] = list1.get(ANCHOR) 

    output = display_current(data, "visitors", user_select["apt"])

    for out in json.loads(output):
        list2.insert(END, out) 
    list2.bind("<<ListboxSelect>>", item2_picked)

for item1 in aptlist:
    list1.insert(END, item1)
list1.bind("<<ListboxSelect>>", item1_picked)

def signin():
    visitors = []
    visitors.append(user_select["visitors"])
    print (visitors)
    sign_in_to_file(user_select["apt"], visitors)
     
def signout():
    print (user_select["apt"])
    sign_out_to_file(user_select["apt"])

inButton = Button(frame2, text="Sign In", command=signin, fg="blue", bg="red", font=("Helvetica", 14))
inButton.grid(row=2, column=4, sticky="nw")
outButton = Button(frame2, text="Sign Out", command=signout, fg="blue", bg="red", font=("Helvetica", 14))
outButton.grid(row=2, column=4, sticky="sw")

#---------------------------------------------------------------------------------------------
# Exit button
#---------------------------------------------------------------------------------------------
exitButton = Button(root, text="Exit", command=root.quit, fg="blue", bg="red", font=("Helvetica", 14))
exitButton.pack(pady=20)

root.mainloop()