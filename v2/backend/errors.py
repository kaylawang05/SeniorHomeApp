class Error(Exception): pass

class ApartmentNotFound(Error): pass

class TenantNotFound(Error): pass
class VisitorNotFound(Error): pass

class DuplicateTenant(Error): pass
class DuplicateVisitor(Error): pass

class VisitorAlreadySignedIn(Error): pass
class VisitorNotSignedIn(Error): pass