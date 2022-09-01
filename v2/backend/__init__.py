from returns.result import Failure, Result, Success

from backend.apartment import (
    Apartment,
    ApartmentDatabase,
    ApartmentDecoder,
    ApartmentEncoder,
)
from backend.errors import (
    ApartmentNotFound,
    DuplicateTenant,
    DuplicateVisitor,
    Error,
    TenantNotFound,
    VisitorNotFound,
    VisitorNotSignedIn,
)
from backend.visit import VisitorManager, date_today
