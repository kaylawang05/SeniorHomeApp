from dataclasses import dataclass
import json
from typing import Tuple

from fuzzywuzzy import process
from returns.result import Result, Failure, Success

from errors import Error

@dataclass
class Apartment:
    number: int
    tenants: list[str]
    visitors: list[str]

class ApartmentEncoder(json.JSONEncoder):
    def default(self, o: Apartment) -> dict:
        if isinstance(o, Apartment):
            return {
                "number": o.number,
                "tenants": o.tenants,
                "visitors": o.visitors,
            }
        return json.JSONEncoder.default(self, o)

class ApartmentDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct: dict) -> Apartment:
        return Apartment(
            number = dct["number"],
            tenants = dct["tenants"],
            visitors = dct["visitors"],
        )

class ApartmentDatabase:
    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            self.rows: list[Apartment] = json.load(f, cls=ApartmentDecoder)
        self.apt_to_row = {apt.number: i for i, apt in enumerate(self.rows)}

    def get_apt(self, number: int) -> Result[Apartment, Error]:
        if number not in self.apt_to_row:
            return Failure(Error.ApartmentNotFound)
        rn = self.apt_to_row[number]
        return Success(self.rows[rn])
            
    def save(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(self.rows, cls=ApartmentEncoder))
    
    def query(self, query, limit: int = -1) -> list[Tuple[Apartment, int]]:
        return process.extract(str(query), self.rows, limit=len(self.rows) if limit == -1 else limit)

    def remove_visitor(self, number: int, name: str) -> Result[None, Error]:
        match self.get_apt(number):
            case Success(apt):
                if name not in apt.visitors:
                    return Failure(Error.VisitorNotFound)
                apt.visitors.remove(name)
            case Failure(x):
                return Failure(x)
        return Success(None)

    def add_visitor(self, number: int, name: str) -> Result[None, Error]:
        match self.get_apt(number):
            case Success(apt):
                if name in apt.visitors:
                    return Failure(Error.DuplicateVisitor)
                apt.visitors.append(name)
            case Failure(x):
                return Failure(x)
        return Success(None)

    def remove_tenant(self, number: int, name: str) -> Result[None, Error]:
        match self.get_apt(number):
            case Success(apt):
                if name not in apt.tenants:
                    return Failure(Error.TenantNotFound)
                apt.tenants.remove(name)
            case Failure(x):
                return Failure(x)
        return Success(None)
 
    def add_tenant(self, number: int, name: str) -> Result[None, Error]:
        match self.get_apt(number):
            case Success(apt):
                if name in apt.tenants:
                    return Failure(Error.DuplicateTenant)
                apt.tenants.append(name)
            case Failure(x):
                return Failure(x)
        return Success(None)