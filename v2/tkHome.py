import tkinter as tk
import sys
import os
from tkinter import *
from PIL import ImageTk

bg_color = "#cd661d"


def openSignIn():
    root.destroy()
    os.system('python3 tkSignIn.py')  # calls the tkSignIn.py python script


def openSignOut():
    root.destroy()
    os.system('python3 tkSignOut.py')  # calls the tkSignOut.py python script


def openUpdateProfile():
    root.destroy()
    # calls the tkUpdateProfile.py python script
    os.system('python3 tkUpdateProfile.py')


# initialize app
root = tk.Tk()
root.title("Springfield Senior Center Homepage")
root.eval("tk::PlaceWindow . center")

# creating a frame widget
homeFrame = tk.Frame(root, width=1310, height=980, bg=bg_color)
homeFrame.grid(row=0, column=0)
homeFrame.pack_propagate(False)

# homeFrame widgets
logo_img = ImageTk.PhotoImage(
    file="./images/frontentrance.jpeg")  # homepage image
logo_widget = tk.Label(homeFrame, image=logo_img, bg=bg_color)
logo_widget.image = logo_img
logo_widget.pack()  # pack method

# label widget
tk.Label(homeFrame, text="Welcome to the Springfield Senior Center Page!",
         bg=bg_color,
         fg="white",
         font=("TkMenuFont", 16)
         ).pack(pady=10)

# button widget
tk.Button(homeFrame, text="SIGN-IN",
          font=("TkHeadingFont", 20),
          bg="#28393a",
          fg="white",
          cursor="hand2",
          activebackground="#e3cf57",
          activeforeground="black",
          command=openSignIn
          ).pack(pady=20)

tk.Button(homeFrame, text="SIGN-OUT",
          font=("TkHeadingFont", 20),
          bg="#28393a",
          fg="white",
          cursor="hand2",
          activebackground="#e3cf57",
          activeforeground="black",
          command=openSignOut
          ).pack(pady=20)

tk.Button(homeFrame, text="UPDATE PROFILE",
          font=("TkHeadingFont", 20),
          bg="#28393a",
          fg="white",
          cursor="hand2",
          activebackground="#e3cf57",
          activeforeground="black",
          command=openUpdateProfile
          ).pack(pady=20)

# run app // displays window until EXIT
root.mainloop()
