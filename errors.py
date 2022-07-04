from enum import Enum

class Error(Enum):
    ApartmentNotFound = 0
    VisitorNotFound = 1
    DuplicateVisitor = 2
    TenantNotFound = 3
    DuplicateTenant = 4
