class Error(Exception): pass

class ApartmentNotFound(Error): pass
class VisitorNotFound(Error): pass
class DuplicateVisitor(Error): pass
class TenantNotFound(Error): pass
class DuplicateTenant(Error): pass