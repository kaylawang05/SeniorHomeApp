from dataclasses import dataclass
import json

from fuzzywuzzy import process
from returns.result import Result, Failure, Success

from dataclasses import dataclass
import json

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

    def get_apt(self, apt: int) -> Result[Apartment, str]:
        if apt not in self.apt_to_row:
            return Failure(f"Apartment '{apt}' not found in database")
        
        rn = self.apt_to_row[apt]

        return Success(self.rows[rn])
            
    def save(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(self.rows, cls=ApartmentEncoder))
    
    def query(self, query, limit=5) -> list[Apartment]:
        return process.extract(str(query), self.rows, limit=limit)

    def remove_visitor(self, number: int, name: str) -> Result[None, str]:
        match self.get_apt(number):
            case Success(apt):
                if name not in apt.visitors:
                    return Failure(f"'{name}' is not a visitor of apartment '{number}'")
                apt.visitors.remove(name)
            case Failure(x):
                return Failure(x)
        return Success(None)

    def add_visitor(self, number: int, name: str) -> Result[None, str]:
        match self.get_apt(number):
            case Success(apt):
                apt.visitors.append(name)
            case Failure(x):
                return Failure(x)
        return Success(None)

    def remove_tenant(self, number: int, name: str) -> Result[None, str]:
        match self.get_apt(number):
            case Success(apt):
                if name not in apt.tenants:
                    return Failure(f"'{name}' is not a tenant of apartment '{number}'")
                apt.tenants.remove(name)
            case Failure(x):
                return Failure(x)
        return Success(None)
 
    def add_tenant(self, number: int, name: str) -> Result[None, str]:
        match self.get_apt(number):
            case Success(apt):
                apt.tenants.append(name)
            case Failure(x):
                return Failure(x)
        return Success(None)