from tkinter import *  # type: ignore

from returns.result import Failure, Result, Success

from backend.apartment import ApartmentDatabase, Error
from backend.visit import VisitorManager

def main():
    apts = ApartmentDatabase("./data/apt.json")

    root = Tk()

    e = Entry(root, width=50, borderwidth=5)
    e.pack()

    def clear():
        list = root.pack_slaves()
        for l in list:
            if type(l) == Label:
                l.destroy()

    def search(key):
        clear()
        results = apts.query(e.get())
        for (apt, score) in results:
            label = Label(root, text=f"{apt.number},{apt.tenants},{apt.visitors},{score}")
            label.pack()
    
    #e.bind("<KeyPress>", search)
    e.bind("<KeyRelease>", search)

    root.mainloop()

if __name__ == "__main__":
    main()
