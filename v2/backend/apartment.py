import json
from typing import Tuple

from fuzzywuzzy import process

from backend.errors import *
from backend.objects import *

class ApartmentManager:
    def __init__(self, path: str):
        self.path = path

        with open(path, "r") as f:
            self.rows: list[Apartment] = json.load(f, cls=ApartmentDecoder)
        
        self.apt_to_row = {apt.number: i for i, apt in enumerate(self.rows)}

    def save(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.rows, cls=ApartmentEncoder))

    def get_apt(self, number: int) -> Apartment:
        if number not in self.apt_to_row:
            raise ApartmentNotFound(f"Could not find apartment '{number}' in database of known apartments.")
        return self.rows[self.apt_to_row[number]]
    
    def get_numbers(self) -> list[int]:
        return list(self.apt_to_row.keys())

    def get_tenants(self, number: int) -> list[str]:
        if number not in self.apt_to_row:
            raise ApartmentNotFound(f"Could not find apartment '{number}' in database of known apartments.")
        return self.rows[self.apt_to_row[number]].tenants
    
    def get_visitors(self, number: int) -> list[Visitor]:
        if number not in self.apt_to_row:
            raise ApartmentNotFound(f"Could not find apartment '{number}' in database of known apartments.")
    
        return self.rows[self.apt_to_row[number]].visitors
    
    def query(self, query, limit: int = -1) -> list[Tuple[Apartment, int]]:
        return process.extract(str(query), self.rows, limit=len(self.rows) if limit == -1 else limit)

    def add_tenant(self, name: str, number: int):
        tenants = self.get_tenants(number)
        
        if name in tenants:
            raise DuplicateTenant(f"Could not add tenant '{name}' to apartment '{number}' because there is an exact duplicate tenant.")
        
        tenants.append(name)

        self.save()

    def remove_tenant(self, name: str, number: int):
        tenants = self.get_tenants(number)
       
        if name not in tenants:
            raise TenantNotFound(f"Could not remove tenant '{name}' because he/she was not found in apartment '{number}'.")
       
        tenants.remove(name)

        self.save()
    
    def add_visitor(self, name: str, number: int):
        visitors = self.get_visitors(number)

        if name in visitors:
            raise DuplicateVisitor(f"Could not add visitor '{name}' to apartment '{number}' because there is a visitor with the same name.")
    
        visitors.append(Visitor(name, signed_in=False, history=[]))

        self.save()

    def remove_visitor(self, name: str, number: int):
        visitors = self.get_visitors(number)

        if name not in visitors:
            raise VisitorNotFound(f"Could not remove visitor '{name}' because he/she is not a visitor of apartment '{number}'.")
        
        for v in visitors:
            if v.name == name:
                visitors.remove(v)
                self.save()
                return

    def sign_in(self, name: str, number: int):
        visitors = self.get_visitors(number)

        v = query_name(name, visitors)

        if v == None:
            visitors.append(
                Visitor(
                    name = name,
                    signed_in = True,
                    history = [TimeInterval(begin=datetime.datetime.now(), end="")]
                )
            )
        else:
            if v.signed_in:
                raise VisitorAlreadySignedIn(f"Could not sign in visitor '{name}' because he/she is already signed in to apartment '{number}'")
            t = TimeInterval(begin=datetime.datetime.now(), end="")
            v.signed_in = True
            v.history.append(t)
            
        self.save()

    def sign_out(self, name: str, number: int):
        visitors = self.get_visitors(number)

        v = query_name(name, visitors)

        if v == None:
            raise VisitorNotFound(f"Could not sign out visitor '{name}' because he/she is not a visitor of apartment '{number}'")

        if not v.signed_in:
            raise VisitorNotSignedIn(f"Could not sign out visitor '{name}' because he/she is not signed in to apartment '{number}'")

        for v in visitors:
            if v.name == name:
                v.signed_in = False
                v.history[-1].end = datetime.datetime.now()
        
        self.save()

def query_name(name: str, visitors: list[Visitor]) -> Visitor | None:
    for v in visitors:
        if v.name == name:
            return v