import smtplib
from email.message import EmailMessage
from tkinter import *

from backend import *


def run():
    root = Tk()
    root.title("Springfield Senior Home")
    root.eval("tk::PlaceWindow . center")
    root.configure(bg="#fae5ac")

    e = Entry(root, width=50, highlightthickness=1)
    e.configure(bg="white", fg="black")
    e.pack()

    def click():
        email = e.get()
        myLabel = Label(root, text="email sent")
        myLabel.pack()
        # Email stuff
        date = date_today()
        msg = EmailMessage()
        msg["Subject"] = "Log delivery for " + date
        msg["From"] = "dha@xoba.com"
        # Subject to Change
        msg["To"] = email

        # msg.set_content("Test email")
        with open("visitor-logs/" + date + ".csv", "rb") as f:
            file_data = f.read()
            print("File data in binary", file_data)
            file_name = f.name
            print("File name is", file_name)
            # line below is the problem, you need more perameters thats all dw
            msg.add_attachment(
                file_data, maintype="application", subtype="csv", filename=file_name
            )
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        with open("password.txt", "r") as f:
            server.login("dha@xoba.com", f.read().strip())
        print("Login succeeded")
        server.send_message(msg)
        print("email sent")
        server.quit()

    myButton = Button(root, text="Send", command=click)
    myButton.configure(bg="#fae5ac", highlightbackground="#fae5ac", fg="black")
    myButton.pack()

    root.mainloop()


if __name__ == "__main__":
    run()
