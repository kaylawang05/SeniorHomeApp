import datetime
import os
from backend.errors import *
from backend.apartment import *

class VisitorManager:
    def __init__(self, apts: ApartmentDatabase, path: str):
        self.apts = apts
        self.path = path
        # map of (name, number) -> (line number, sign in time)
        self.visitors: dict[Tuple[str, int], Tuple[str, int]] = {}
        self.current_line = 0
    
    def sign_in(self, name: str, number: int) -> Result[None, ApartmentNotFound | DuplicateVisitor | VisitorAlreadySignedIn]:
        if (name, number) in self.visitors:
            return Failure(VisitorAlreadySignedIn(f"Cannot sign in visitor '{name}' because he/she is already signed in to apartment '{number}'"))

        match self.apts.get_visitors(number):
            case Success(visitors):
                if name not in visitors:
                    match self.apts.add_visitor(name, number):
                        case Failure(x):
                            return Failure(x)
            case Failure(x):
                return Failure(x)
        
        with open(os.path.join(self.path, f"{datetime.datetime.today()}.csv"), "a+") as f:
            if f.read() == "":
                f.write("Apartment Number,Name,Sign In Time,Sign Out Time")
                self.current_line = 0
            
            sign_in_time = datetime.datetime.now().strftime("%H:%M")

            self.visitors[(name, number)] = (sign_in_time, self.current_line)
            self.current_line += 1

            f.write(f"{number},{name},{sign_in_time}")

        return Success(None)
    
    def sign_out(self, name: str, number: int) -> Result[None, ApartmentNotFound | VisitorNotFound | VisitorNotSignedIn]:
        match self.apts.get_visitors(number):
            case Success(visitors):
                if name not in visitors:
                    return Failure(VisitorNotFound(f"Could not sign out visitor '{name}' because he/she is not a visitor of apartment '{number}'"))
            case Failure(x):
                return Failure(x)
        
        if (name, number) not in self.visitors:
            return Failure(VisitorNotSignedIn(f"Could not sign out visitor '{name}' because he/she is not signed in to apartment '{number}'"))

        # right now doesn't handle the edge case of signing in on one day and signing out the other day, but that is fine for now
        with open(os.path.join(self.path, f"{datetime.datetime.today()}.csv"), "w+") as f:
            if f.read() == "":
                f.write("Apartment Number,Name,Sign In Time,Sign Out Time")
                self.current_line = 0
            
            sign_out_time = datetime.datetime.now().strftime("%H:%M")

            sign_in_time, line = self.visitors[(name, number)]

            lines = f.readlines()

            lines[line] += f",{sign_out_time}"

            f.write("".join(lines))

        del self.visitors[(name, number)]

        return Success(None)




        return Success(None)