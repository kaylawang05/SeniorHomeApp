import os
from tkinter import *
from backend import *
import json

root = Tk()
root.title('Springfield Senior Home')
root.geometry("500x700")


def displayTenants(number: int):
    apt = apts.get_apt(number).unwrap()
    tenantList.delete(0, END)
    if not apt.tenants:
        message.config(
            text="There are no registered tenants for this apartment.")
    # Try to code to only insert visitors signed in already
    for tenant in apt.tenants:
        tenantList.insert(END, tenant)


def displayVisitors(number: int):
    apt = apts.get_apt(number).unwrap()
    visitorList.delete(0, END)
    if not apt.visitors:
        message.config(
            text="There are no registered visitors for this apartment.")
    # Try to code to only insert visitors signed in already
    for visitor in apt.visitors:
        visitorList.insert(END, visitor)

# Outputs list of visitors of a given apartment #


def enter():
    message.config(text="")
    number = int(aptNumber.get())
    # I will deal with invalid apartment numbers later
    match apts.get_apt(number):
        case Success():
            displayVisitors(number)
            displayTenants(number)

        case Failure():
            message.config(
                text="Please enter a valid apartment number.\nAsk help from the guard if necessary.")


def addTenant():
    number = int(aptNumber.get())
    apts.add_tenant(tenantEntry.get(), number)
    displayTenants(number)
    tenantEntry.delete(0, END)


def deleteTenant():
    number = int(aptNumber.get())
    name = tenantList.get(ANCHOR)
    apts.remove_tenant(name, number)
    displayTenants(number)


def addVisitor():
    number = int(aptNumber.get())
    apts.add_visitor(visitorEntry.get(), number)
    displayVisitors(number)
    visitorEntry.delete(0, END)


def deleteVisitor():
    number = int(aptNumber.get())
    name = visitorList.get(ANCHOR)
    apts.remove_visitor(name, number)
    displayVisitors(number)


# Help message that appears when help button is clicked
def help():
    message.config(text="Enter the apartment number to update its profile\n \
Click 'Enter'.\nYou will see a list of all the registered tenants and visitors in the boxes above.\n \
To add a tenant or visitor, enter the name in the box below the list\nClick 'Add'.\n \
To delete a tenant or visitor, click on the name. \n Click 'Delete'\n")

# I don't know how to go back to the home page so I will make the app close for now


def back():
    os.system("python3 tkHome.py")
    quit()


# Code for how the app appears
title = Label(root, text="Update Profile", font=("Helvetica", 20))
title.pack(side=TOP, pady=5)

apts = ApartmentDatabase("./data/apts.json")
allVisitors = VisitorManager(apts, "./visitor-logs/")

prompt = Label(root, text="Enter apartment #:")
prompt.pack()

aptNumber = Entry(root, width=10)
aptNumber.pack()

enter_btn = Button(root, text="Enter", command=enter)
enter_btn.pack(pady=5)

# create a frame with the labels side by side
labelFrame = Frame(root, width=500, height=10)
labelFrame.pack(pady=(10, 0))

tenantLabel = Label(labelFrame, text="Tenants")
tenantLabel.pack(side=LEFT, pady=10, padx=50)

visitorLabel = Label(labelFrame, text="Visitors")
visitorLabel.pack(side=RIGHT, pady=10, padx=50)

# create a frame with the listboxes side by side
listFrame = Frame(root, width=500, height=100)
listFrame.pack()

tenantList = Listbox(listFrame)
tenantList.pack(side=LEFT, padx=10)

visitorList = Listbox(listFrame)
visitorList.pack(side=RIGHT, padx=10)

# create a frame with the entrys side by side
entryFrame = Frame(root, width=500, height=50)
entryFrame.pack()

tenantEntry = Entry(entryFrame)
tenantEntry.pack(side=LEFT, pady=10, padx=10)

visitorEntry = Entry(entryFrame)
visitorEntry.pack(side=RIGHT, pady=10, padx=10)


# create a frame with the add and delete buttons
buttonFrame = Frame(root, width=500, height=50)
buttonFrame.pack()

leftFrame = Frame(buttonFrame, width=250, height=50)
leftFrame.pack(side=LEFT, padx=(100, 10))

rightFrame = Frame(buttonFrame, width=250, height=50)
rightFrame.pack(side=RIGHT, padx=(10, 100))

tenantAdd = Button(leftFrame, text="Add", command=addTenant)
tenantAdd.pack(side=LEFT, pady=10, padx=10)

tenantDelete = Button(leftFrame, text="Delete", command=deleteTenant)
tenantDelete.pack(side=RIGHT, pady=10, padx=10)

visitorAdd = Button(rightFrame, text="Add", command=addVisitor)
visitorAdd.pack(side=LEFT, pady=10, padx=10)

visitorDelete = Button(rightFrame, text="Delete", command=deleteVisitor)
visitorDelete.pack(side=RIGHT, pady=10, padx=10)

# rest of buttons
helpButton = Button(root, text="Help", command=help)
helpButton.pack(pady=5)

backButton = Button(root, text="Back", command=back)
backButton.pack(pady=5)

global message
message = Label(root, text="")
message.pack(pady=5)

root.mainloop()
