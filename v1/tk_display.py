#!/usr/bin/python3
from cgitb import text
import json
from tkinter import *
#from tkinter import ttk
from displayAptInfo import display_current
from updateTenants import backup_copy

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
title = Label(root, text="Tenant Profile Page", font=("Helvetica", 20))
title.pack(side=TOP, pady=50)

#---------------------------------------------------------------------------------------------
# The frame for the list boxes
#---------------------------------------------------------------------------------------------
frame2 = Frame(root)
frame2.pack(pady=20)

l1lab = Label(frame2, text="Apt Numbers", justify=LEFT, font=("Helvetica", 14))
l1lab.grid(row=1, column=0, sticky="w", padx=5)
l2lab = Label(frame2, text="Items", justify=LEFT, font=("Helvetica", 14))
l2lab.grid(row=1, column=1, sticky= "w", padx=25)
l3lab = Label(frame2, text="Content", justify=LEFT, font=("Helvetica", 14))
l3lab.grid(row=1, column=2, sticky="w", padx=20)

list1 = Listbox(frame2)
list2 = Listbox(frame2)
list3 = Listbox(frame2)
list1.grid(row=2, column=0, sticky="w")
list2.grid(row=2, column=1, padx=20, sticky="w")
list3.grid(row=2, column=2, padx=5, sticky="w")
#list1_scrollbar = Scrollbar(frame2, orient=VERTICAL)
#list1_scrollbar.config(command=list1.yview)
#list1_scrollbar.pack(side=RIGHT, fill=Y)

user_select = { "apt": "", "item": "", "content": ""}

def item3_picked(e):
    user_select["content"] = list3.get(ANCHOR)

def item2_picked(e):
    list3.delete('0', 'end')
    user_select["item"] = list2.get(ANCHOR) 
    
    output = display_current(data, user_select["item"], user_select["apt"])

    for out in json.loads(output):
        list3.insert(END, out) 
    list3.bind("<<ListboxSelect>>", item3_picked)

def item1_picked(e):
    list2.delete('0', 'end')
    list3.delete('0', 'end')
    user_select["apt"] = list1.get(ANCHOR) 

    for item2 in ("tenants", "visitors", "car_plates"):
        list2.insert(END, item2) 
    list2.bind("<<ListboxSelect>>", item2_picked)

for item1 in aptlist:
    list1.insert(END, item1)
list1.bind("<<ListboxSelect>>", item1_picked)

# Add entry
e1 = Entry(frame2)
e1.grid(row=2, column=4, sticky="w")

def add_item():
    backup_copy()
    new = e1.get()
    print ("New item is: " + new)
    for i in data:
        if i["aptnum"] == user_select["apt"]:
            i[user_select["item"]].append(new)
            e1.delete(0, 'end')
            break
    # Write data to apt.json
    with open(aptJsonFile, 'w') as file:
        json.dump(data, file)
    file.close()
     
def delete_item():
    backup_copy()
    itemToDel = user_select["content"]
    print ("Item to delete is: " + itemToDel)
    for (data_index, unit) in enumerate(data):
        if unit["aptnum"] == user_select["apt"]:
            data[data_index][user_select["item"]].remove(user_select["content"])
            break
    # Write data to apt.json
    with open(aptJsonFile, 'w') as file:
        json.dump(data, file)
    file.close()

addButton = Button(frame2, text="Add", command=add_item, fg="blue", bg="red", font=("Helvetica", 14))
addButton.grid(row=2, column=4, sticky="nw")
delButton = Button(frame2, text="Delete", command=delete_item, fg="blue", bg="red", font=("Helvetica", 14))
delButton.grid(row=2, column=4, sticky="sw")

#---------------------------------------------------------------------------------------------
# Exit button
#---------------------------------------------------------------------------------------------
exitButton = Button(root, text="Exit", command=root.quit, fg="blue", bg="red", font=("Helvetica", 14))
exitButton.pack(pady=20)

root.mainloop()