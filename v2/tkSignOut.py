# To-do list:
# 1. Figuring out how to code the back button to go to a different page
# 2. Only display visitors that are signed in
# 3. Formatting

from tkinter import *
from backend import *

root = Tk()
root.title('Springfield Senior Home')
root.geometry("500x700")

# Outputs list of visitors of a given apartment #
def enter():
    message.config(text="")
    number = int(aptNumber.get())
    # I will deal with invalid apartment numbers later
    match apts.get_apt(number):
        case Success():
            visitorList.delete(0, END)
            apt = apts.get_apt(number).unwrap()
            if not apt.visitors:
                message.config(text="There are no registered visitors for this apartment.")
            # Try to code to only insert visitors signed in already
            for visitor in apt.visitors:
                visitorList.insert(END, visitor)
        case Failure():
            visitorList.delete(0, END)
            message.config(text="Please enter a valid apartment number.\nAsk help from the guard if necessary.")

# Signs out the selected visitor if the visitor is signed in
def signOut():
    number = int(aptNumber.get())
    name = visitorList.get(ANCHOR)
    allVisitors.sign_in(number, name)
    match allVisitors.sign_out(number, name):
        case Success():
            allVisitors.sign_out(number, name)
            message.config(text=name + " has successfully signed out.")
        case Failure():
            message.config(text="This visitor is not signed in in the first place.")

# Help message that appears when help button is clicked
def help():
    message.config(text="To sign out, enter the apartment number of the visitor.\n \
Click 'Enter'.\nYou will see a list of all the registered visitors in the box above.\n \
Click on the visitor that you want to sign out.\nClick 'Sign out'.\n \
If you don't see your name, please register yourself as a visitor in the sign in page.")

# I don't know how to go back to the home page so I will make the app close for now
def back():
    root.destroy()

# Code for how the app appears
title = Label(root, text="Sign Out", font=("Helvetica", 20))
title.pack(side=TOP, pady=5)

apts = ApartmentDatabase("./data/apt.json")
allVisitors = VisitorManager(apts, "./visitor-logs/")

prompt = Label(root, text="Enter apartment #:")
prompt.pack()

aptNumber = Entry(root, width=10)
aptNumber.pack()

enter = Button(root, text="Enter", command=enter)
enter.pack(pady=5)

visitorList = Listbox(root)
visitorList.pack(pady=10)

signOutButton = Button(root, text="Sign out", command=signOut)
signOutButton.pack(pady=5)

helpButton = Button(root, text="Help", command=help)
helpButton.pack(pady=5)

backButton = Button(root, text="Back", command=back)
backButton.pack(pady=5)

global message
message = Label(root, text="")
message.pack(pady=5)

root.mainloop()
