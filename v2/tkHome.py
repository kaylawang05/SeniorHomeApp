import tkinter as tk
from tkinter import *

from PIL import ImageTk

import logEmail
import tkSignIn
import tkSignOut
import tkUpdateProfile

bg_color = "#FAE5AC"
button_color = "#cd661d"


def openSignIn():
    tkSignIn.run()  # calls the tkSignIn.py python script


def openSignOut():
    tkSignOut.run()  # calls the tkSignOut.py python script


def openUpdateProfile():
    tkUpdateProfile.run()  # calls the tkUpdateProfile.py python script


def openLog():
    logEmail.run()  # calls the tkVisitorLog.py python script


# initialize app
root = tk.Tk()
root.title("Springfield Senior Center Homepage")
root.eval("tk::PlaceWindow . center")

# creating a frame widget
homeFrame = tk.Frame(root, highlightbackground="#cd661d",
                     highlightthickness=5, width=1000, height=1000, bg=bg_color)
homeFrame.grid(row=0, column=0)
homeFrame.pack_propagate(False)

# label widget
title = tk.Label(homeFrame, text="Welcome to the Springfield Senior Center Page!",
                 bg=bg_color,
                 fg="#5F5F9E",
                 font=("TkMenuFont", 30, 'bold')
                 ).pack(pady=1)

# button widgets
sInButton = tk.Button(homeFrame, text="  SIGN-IN  ",
                      font=("TkHeadingFont", 28),
                      bg=button_color,
                      fg="white",
                      cursor="hand2",
                      activebackground="#FFFF7F",
                      activeforeground="black",
                      command=openSignIn
                      ).place(x=275, y=100)

sOutButton = tk.Button(homeFrame, text="SIGN-OUT",
                       font=("TkHeadingFont", 28),
                       bg=button_color,
                       fg="white",
                       cursor="hand2",
                       activebackground="#FFFF7F",
                       activeforeground="black",
                       command=openSignOut
                       ).place(x=500, y=100)

updtButton = tk.Button(homeFrame, text="UPDATE PROFILE",
                       font=("TkHeadingFont", 14),
                       bg=button_color,
                       fg="white",
                       cursor="hand2",
                       activebackground="#FFFF7F",
                       activeforeground="black",
                       command=openUpdateProfile
                       ).place(x=302, y=200)

logButton = tk.Button(homeFrame, text=" SEND LOG INFO ",
                      font=("TkHeadingFont", 14),
                      bg=button_color,
                      fg="white",
                      cursor="hand2",
                      activebackground="#FFFF7F",
                      activeforeground="black",
                      command=openLog
                      ).place(x=500, y=200)

# homeFrame widgets
# IMAGE DIMENSIONS NEED TO BE 930x432
logo_img = ImageTk.PhotoImage(file="./images/frontentrance.jpeg")
logo_widget = tk.Label(homeFrame, image=logo_img, bg=bg_color)
logo_widget.image = logo_img
logo_widget.pack(side="bottom", pady=100)

# run app // displays window until EXIT
root.mainloop()
