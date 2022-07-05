from dataclasses import dataclass
import os

from returns.result import Result, Failure, Success

from apartment import ApartmentDatabase
from errors import Error
from util import get_time, get_date

@dataclass(unsafe_hash=True)
class Visitor:
    number: int
    name: str

class VisitorManager:
    def __init__(self, apts: ApartmentDatabase, path: str):
        self.apts = apts
        self.path = path
        self.visitors: dict[Visitor, str] = {}

    def get_vistors(self) -> list[Visitor]:
        return list(self.visitors.keys())

    def sign_in(self, number: int, name: str) -> Result[None, Error]:
        match self.apts.add_visitor(number, name):
            case Success(_):
                self.visitors[Visitor(number, name)] = get_time()
                self.apts.save()
            case Failure(Error.DuplicateVisitor):
                self.visitors[Visitor(number, name)] = get_time()
            case Failure(x):
                return Failure(x)
        return Success(None)

    def sign_out(self, number: int, name: str) -> Result[None, Error]:
        v = Visitor(number, name)
        if v in self.visitors:
            self.add_log(f"{number},{name},{self.visitors[v]},{get_time()}")
            self.visitors.pop(v)
            return Success(None)
        else:
            return Failure(Error.VisitorNotFound)

    # could happen that the name has a comma in it and this breaks, but frontend will filter that :)
    def add_log(self, text):
        with open(os.path.join(self.path, f"{get_date()}.csv"), "a+") as f:
            f.write(text+"\n")