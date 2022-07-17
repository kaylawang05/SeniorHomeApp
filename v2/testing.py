import json
import pathlib

import pytest

from backend import *

@pytest.fixture
def apts(tmp_path: pathlib.Path) -> ApartmentDatabase:
    f = tmp_path / "test_apts.json"
    rows = [Apartment(number=69, tenants=['alice', 'bob', 'cindy'], visitors=['david', 'ethan', 'frank', 'bruh']), Apartment(number=420, tenants=['alex', 'ben', 'catherine'], visitors=['daniel', 'elise', 'francis']), Apartment(number=101, tenants=['Tanya'], visitors=['John Watson', 'Mary Watson']), Apartment(number=102, tenants=['Mike Bowen'], visitors=['Tom']), Apartment(number=103, tenants=['Gail Lee'], visitors=[]), Apartment(number=104, tenants=[], visitors=[]), Apartment(number=105, tenants=[], visitors=[]), Apartment(number=201, tenants=['john', 'mary'], visitors=['Jerry', 'Eric Wang', 'Tom']), Apartment(number=202, tenants=[], visitors=[]), Apartment(number=203, tenants=[], visitors=[]), Apartment(number=204, tenants=[], visitors=[]), Apartment(number=205, tenants=[], visitors=['Barack Obama']), Apartment(number=301, tenants=[], visitors=[]), Apartment(number=302, tenants=[], visitors=[]), Apartment(number=303, tenants=[], visitors=[]), Apartment(number=304, tenants=[], visitors=[]), Apartment(number=305, tenants=[], visitors=[])]
    f.write_text(json.dumps(rows, cls=ApartmentEncoder))
    return ApartmentDatabase(str(f))

@pytest.fixture
def visitors(tmp_path: pathlib.Path, apts: ApartmentDatabase) -> VisitorManager:
    d = tmp_path / "test_visitor_logs"
    d.mkdir()
    return VisitorManager(apts, str(d))

def test_get_apt(apts: ApartmentDatabase):
    assert apts.get_apt(69) == Success(Apartment(
        number = 69,
        tenants = ["alice", "bob", "cindy"],
        visitors = ["david", "ethan", "frank", "bruh"],
    ))

def test_get_numbers(apts: ApartmentDatabase):
    assert apts.get_numbers() == [69, 420, 101, 102, 103, 104, 105, 201, 202, 203, 204, 205, 301, 302, 303, 304, 305]

def test_get_tenants(apts: ApartmentDatabase):
    assert apts.get_tenants(420) == Success(['alex', 'ben', 'catherine'])

def test_get_visitors(apts: ApartmentDatabase):
    assert apts.get_visitors(101) == Success(['John Watson', 'Mary Watson'])

def test_sign_in(visitors: VisitorManager):
    visitors.sign_in("david", 102).unwrap()
    visitors.sign_out("david", 102).unwrap()
    visitors.sign_in("bob", 102).unwrap()
    visitors.sign_in("clara", 102).unwrap()
    visitors.sign_out("bob", 102).unwrap()
    visitors.sign_out("clara", 102).unwrap()

# def test_add_visitor(apts: ApartmentDatabase):
#     assert apts.add_visitor("Tom", 102)
#     assert apts.add_visitor("Bill", 102)
#     assert apts.add_visitor("Tom", 3141592653)
