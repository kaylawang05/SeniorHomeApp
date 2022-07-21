import json
from dataclasses import dataclass
from typing import Tuple

from fuzzywuzzy import process
from returns.result import Failure, Result, Success

from backend.errors import *

@dataclass
class Apartment:
    number: int
    tenants: list[str]
    visitors: list[str]

class ApartmentEncoder(json.JSONEncoder):
    def default(self, o) -> dict | str:
        if isinstance(o, Apartment):
            return {
                "number": o.number,
                "tenants": o.tenants,
                "visitors": o.visitors
            }
        return json.JSONEncoder.default(self, o)

class ApartmentDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct: dict) -> Apartment | dict:
        if "tenants" in dct:
            return Apartment(
                number = dct["number"],
                tenants = dct["tenants"],
                visitors = dct["visitors"],
            )
        return dct

class ApartmentDatabase:
    def __init__(self, path: str):
        self.path = path

        with open(path, "r") as f:
            self.rows: list[Apartment] = json.load(f, cls=ApartmentDecoder)
            
        self.apt_to_row = {apt.number: i for i, apt in enumerate(self.rows)}

    def save(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.rows, cls=ApartmentEncoder))

    def get_apts(self) -> list[Apartment]:
        return self.rows

    def get_apt(self, number: int) -> Result[Apartment, ApartmentNotFound]:
        if number not in self.apt_to_row:
            return Failure(ApartmentNotFound(f"Could not find apartment '{number}' in database of known apartments."))
        return Success(self.rows[self.apt_to_row[number]])
    
    def get_numbers(self) -> list[int]:
        return list(self.apt_to_row.keys())

    def get_tenants(self, number: int) -> Result[list[str], ApartmentNotFound]:
        if number not in self.apt_to_row:
            return Failure(ApartmentNotFound(f"Could not find apartment '{number}' in database of known apartments."))
        return Success(self.rows[self.apt_to_row[number]].tenants)
    
    def get_visitors(self, number: int) -> Result[list[str], ApartmentNotFound]:
        if number not in self.apt_to_row:
            return Failure(ApartmentNotFound(f"Could not find apartment '{number}' in database of known apartments."))
        return Success(self.rows[self.apt_to_row[number]].visitors)
    
    def query(self, query, limit: int = -1) -> list[Tuple[Apartment, int]]:
        return process.extract(str(query), self.rows, limit=len(self.rows) if limit == -1 else limit)

    def add_tenant(self, name: str, number: int) -> Result[None, DuplicateTenant | ApartmentNotFound]:
        match self.get_tenants(number):
            case Success(tenants):
                if name in tenants:
                    return Failure(DuplicateTenant(f"Could not add tenant '{name}' to apartment '{number}' because there is an exact duplicate tenant."))
                tenants.append(name)
                self.save()
            case Failure(x):
                return Failure(x)
        return Success(None)
    
    def remove_tenant(self, name: str, number: int) -> Result[None, TenantNotFound | ApartmentNotFound]:
        match self.get_tenants(number):
            case Success(tenants):
                if name not in tenants:
                    return Failure(TenantNotFound(f"Could not remove tenant '{name}' because he/she was not found in apartment '{number}'."))
                tenants.remove(name)
                self.save()
            case Failure(x):
                return Failure(x)
        return Success(None)
    
    def add_visitor(self, name: str, number: int) -> Result[None, DuplicateVisitor | ApartmentNotFound]:
        match self.get_visitors(number):
            case Success(visitors):
                if name in visitors:
                    return Failure(DuplicateVisitor(f"Could not add visitor '{name}' to apartment '{number}' because there is a visitor with the same name."))
                visitors.append(name)
                self.save()
            case Failure(x):
                return Failure(x)        
        return Success(None)
        
    def remove_visitor(self, name: str, number: int) -> Result[None, VisitorNotFound | ApartmentNotFound]:
        match self.get_visitors(number):
            case Success(visitors):
                if name not in visitors:
                    return Failure(VisitorNotFound(f"Could not remove visitor '{name}' because he/she is not a visitor of apartment '{number}'."))
                visitors.remove(name)
                self.save()
            case Failure(x):
                return Failure(x)
        return Success(None) 