import csv
import os
from datetime import datetime

from backend.apartment import *
from backend.errors import *


class VisitorManager:
    def __init__(self, apts: ApartmentDatabase, path: str):
        self.apts = apts
        self.path = path

        self.visitors: dict[Tuple[str, int], Tuple[str, int]] = {}
        self.current_line = 0

        if self.log_exists():
            with open(self.file_path, "r") as f:
                csvreader = csv.reader(f)
                head = next(csvreader)
                for (number, name, sign_in_time, sign_out_time) in csv.reader(f):
                    if sign_out_time == "":
                        self.visitors[(name, int(number))] = (
                            sign_in_time,
                            self.current_line,
                        )
                    self.current_line += 1

    def log_exists(self) -> bool:
        self.file_path = os.path.join(self.path, f"{date_today()}.csv")
        return os.path.exists(self.file_path)

    def sign_in(
        self, name: str, number: int
    ) -> Result[None, ApartmentNotFound | DuplicateVisitor | VisitorAlreadySignedIn]:
        if (name, number) in self.visitors:
            return Failure(
                VisitorAlreadySignedIn(
                    f"Cannot sign in visitor '{name}' because he/she is already signed in to apartment '{number}'"
                )
            )

        match self.apts.get_visitors(number):
            case Success(visitors):
                if name not in visitors:
                    match self.apts.add_visitor(name, number):
                        case Failure(x):
                            return Failure(x)
            case Failure(x):
                return Failure(x)

        if not self.log_exists():
            with open(self.file_path, "x+") as f:
                if f.read() == "":
                    self.current_line = 0
                    f.write("Apartment Number,Name,Sign In Time,Sign Out Time\n")

        with open(self.file_path, "a") as f:
            sign_in_time = time_now()
            self.visitors[(name, number)] = (sign_in_time, self.current_line)
            f.write(f"{number},{name},{sign_in_time},\n")
            self.current_line += 1

        return Success(None)

    def sign_out(
        self, name: str, number: int
    ) -> Result[None, ApartmentNotFound | VisitorNotFound | VisitorNotSignedIn]:
        match self.apts.get_visitors(number):
            case Success(visitors):
                if name not in visitors:
                    return Failure(
                        VisitorNotFound(
                            f"Could not sign out visitor '{name}' because he/she is not a visitor of apartment '{number}'"
                        )
                    )
            case Failure(x):
                return Failure(x)

        if (name, number) not in self.visitors:
            return Failure(
                VisitorNotSignedIn(
                    f"Could not sign out visitor '{name}' because he/she is not signed in to apartment '{number}'"
                )
            )

        sign_in_time, line_number = self.visitors[(name, number)]

        lines = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()

        with open(self.file_path, "w") as f:
            lines[line_number + 1] = lines[line_number + 1][:-1] + time_now() + "\n"
            f.write("".join(lines))

        del self.visitors[(name, number)]

        return Success(None)


def time_now() -> str:
    return datetime.now().strftime("%H:%M")


def date_today() -> str:
    return str(datetime.today().date())
