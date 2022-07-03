import datetime
import os

from databases import ApartmentDatabase

class VisitorManager:
    def __init__(self, apt_database: ApartmentDatabase, log_dir: str):
        self.apt_database = apt_database
        self.log_dir = log_dir
        self.signed_in = []

    def sign_in(self, apt, name):
        sign_in_time = datetime.datetime.now().strftime("%H:%M")

        self.apt_database.add_visitor(apt, name)

        self.signed_in.append((apt, name, sign_in_time))

        self.apt_database.save()

    def sign_out(self, apt, name):
        # format: apt,name,sign in time,sign out time

        sign_out_time = datetime.datetime.now().strftime("%H:%M")

        for a, n, t in self.signed_in:
            if a == apt and n == name:
                self.add_log(f"{apt},{name},{t},{sign_out_time}")
                self.signed_in.remove((a,n,t))
                return

        print(f"error: {name} not found in room {apt}")
        quit()
            
        

    def add_log(self, text):
        date = datetime.date.today()

        with open(os.path.join(self.log_dir, f"{date}.csv"), "a+") as f:
            f.write(text+"\n")