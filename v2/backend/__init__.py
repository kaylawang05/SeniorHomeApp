from returns.result import Result, Failure, Success

from backend.apartment import ApartmentDatabase, Apartment
from backend.visit import VisitorManager

from backend.errors import Error, ApartmentNotFound, VisitorNotFound, TenantNotFound, DuplicateTenant, DuplicateVisitor

from backend.util import get_date, get_time