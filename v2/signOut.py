from tkinter import *
from backend import *

root = Tk()
root.title('Springfield Senior Home')
root.geometry("400x600")

def click():
    number = int(aptNumber.get())
    # I will deal with invalid apartment numbers later
    apt = apts.get_apt(number).unwrap()
    for visitor in apt.visitors:
        visitorList.insert(END, visitor)

def signOut():
    number = int(aptNumber.get())
    name = visitorList.get(ANCHOR)
    visitors.sign_out(number, name)
    message = Label(root, text=name + " has successfully signed out")
    message.pack(pady=5)

title = Label(root, text="Sign Out", font=("Helvetica", 20))
title.pack(side=TOP, pady=5)

apts = ApartmentDatabase("./data/apt.json")
# Asked how to use VisitorManager
visitors = VisitorManager(apts, "./data/apt.json")

prompt = Label(root, text="Enter apartment #:")
prompt.pack()

aptNumber = Entry(root, width=10)
aptNumber.pack()

enter = Button(root, text="Enter", command=click)
enter.pack(pady=5)

visitorList = Listbox(root)
visitorList.pack(pady=10)

signOutButton = Button(root, text="Sign out", command=signOut)
signOutButton.pack(pady=5)

# May need to create listbox

root.mainloop()
