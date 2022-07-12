from returns.result import Failure, Result, Success

from backend.apartment import Apartment, ApartmentDatabase
from backend.errors import (ApartmentNotFound, DuplicateTenant,
                            DuplicateVisitor, Error, TenantNotFound,
                            VisitorNotFound)
from backend.util import get_date, get_time
from backend.visit import VisitorManager
