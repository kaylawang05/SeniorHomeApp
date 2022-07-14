from dataclasses import dataclass
import datetime
import json

@dataclass
class TimeInterval:
    begin: datetime.datetime
    end: datetime.datetime | str

@dataclass
class Visitor:
    name: str
    signed_in: bool
    history: list[TimeInterval]

@dataclass
class Apartment:
    number: int
    tenants: list[str]
    visitors: list[Visitor]

class ApartmentEncoder(json.JSONEncoder):
    def default(self, o) -> dict | str:
        if isinstance(o, Apartment):
            return {
                "number": o.number,
                "tenants": o.tenants,
                "visitors": [
                    {
                        "name": v.name,
                        "signed_in": v.signed_in,
                        "history": [
                            {
                                "begin": t.begin,
                                "end": t.end,
                            } for t in v.history
                        ]
                    } for v in o.visitors
                ]
            }
        if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()
        return json.JSONEncoder.default(self, o)

class ApartmentDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct: dict) -> Apartment | dict:
        if "tenants" in dct:
            return Apartment(
                number = dct["number"],
                tenants = dct["tenants"],
                visitors = [
                    Visitor(
                        name = v["name"],
                        signed_in = v["signed_in"],
                        history = [
                            TimeInterval(
                                datetime.datetime.fromisoformat(t["begin"]),
                                datetime.datetime.fromisoformat(t["end"]) if t["end"] != "" else ""
                            )
                            for t in v["history"]
                        ]
                    ) for v in dct["visitors"]
                ]
            )
        return dct