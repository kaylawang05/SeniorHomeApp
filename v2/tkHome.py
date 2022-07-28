import tkinter as tk
from PIL import ImageTk

bg_color = "#cd661d"


def load_frame2():
    print("Take me to the next page")  # need to link to sign-in page


# initialize app
root = tk.Tk()
root.title("Springfield Senior Center Homepage")
root.eval("tk::PlaceWindow . center")

# creating a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=bg_color)
frame1.grid(row=0, column=0)
frame1.pack_propagate(False)

# frame1 widgets
logo_img = ImageTk.PhotoImage(file="./images/SeniorCenterImage.png")
logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
logo_widget.image = logo_img
logo_widget.pack()  # pack method

# label widget
tk.Label(frame1, text="Welcome to the Springfield Senior Center Page!",
         bg=bg_color,
         fg="white",
         font=("TkMenuFont", 16)
         ).pack(pady=10)

# button widget
tk.Button(frame1, text="SIGN-IN HERE",
          font=("TkHeadingFont", 20),
          bg="#28393a",
          fg="white",
          cursor="hand2",
          activebackground="#e3cf57",
          activeforeground="black",
          command=lambda: load_frame2()
          ).pack(pady=20)

# run app // displays window until EXIT
root.mainloop()
