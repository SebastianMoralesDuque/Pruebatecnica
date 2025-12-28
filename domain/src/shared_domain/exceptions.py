class DomainError(Exception):
    """Base class for domain exceptions"""
    pass

class BusinessRuleError(DomainError):
    """Exception raised for business rule violations"""
    pass

class EntityNotFoundError(DomainError):
    """Exception raised when an entity is not found"""
    pass

class InvalidNITError(BusinessRuleError):
    """Raised when the NIT format or value is invalid"""
    pass

class InvalidPriceError(BusinessRuleError):
    """Raised when prices are invalid (negative, non-numeric, etc)"""
    pass

class InfrastructureError(DomainError):
    """Raised when a domain operation fails due to external infrastructure (AI, Blockchain, etc)"""
    pass
