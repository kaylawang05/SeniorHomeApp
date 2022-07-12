import os
from typing import Tuple

from returns.result import Failure, Result, Success

from backend.apartment import ApartmentDatabase
from backend.errors import *
from backend.util import get_date, get_time

class VisitorManager:
    def __init__(self, apts: ApartmentDatabase, path: str):
        self.apts = apts
        self.path = path
        self.visitors: dict[Tuple[int, str], str] = {}

    def add_visitor(self, number: int, name: str):
        self.visitors[(number, name)] = get_time()

    def get_vistors(self) -> list[Tuple[int, str]]:
        return list(self.visitors.keys())

    def is_visitor(self, number: int, name: str) -> bool:
        return (number, name) in self.visitors

    # TODO: write to the file on sign-in
    def sign_in(self, number: int, name: str) -> Result[None, Error]:
        match self.apts.add_visitor(number, name):
            case Success(_):
                self.add_visitor(number, name)
                self.apts.save()
            case Failure(DuplicateVisitor()):
                self.add_visitor(number, name)
            case Failure(x):
                return Failure(x)
        return Success(None)

    def sign_out(self, number: int, name: str) -> Result[None, Error]:
        if (number, name) in self.visitors:
            self.add_log(f"{number},{name},{self.visitors[(number, name)]},{get_time()}")
            self.visitors.pop((number, name))
            return Success(None)
        else:
            return Failure(VisitorNotFound(f"Could not find and sign-out visitor '{name}'"))

    def add_log(self, text):
        with open(os.path.join(self.path, f"{get_date()}.csv"), "a+") as f:
            f.write(text+"\n")
