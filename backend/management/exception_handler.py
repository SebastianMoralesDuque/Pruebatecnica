from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from shared_domain.exceptions import (
    BusinessRuleError, 
    EntityNotFoundError, 
    DomainError,
    InvalidNITError,
    InvalidPriceError,
    InfrastructureError
)

def global_exception_handler(exc, context):
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # Specific Business exceptions mapping to 400
    if isinstance(exc, (BusinessRuleError, InvalidNITError, InvalidPriceError)):
        return Response(
            {
                "error": str(exc), 
                "code": exc.__class__.__name__
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Infrastructure failures mapping to 503 or 500
    if isinstance(exc, InfrastructureError):
        return Response(
            {
                "error": "Servicio externo no disponible",
                "detail": str(exc),
                "code": "InfrastructureError"
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    if isinstance(exc, EntityNotFoundError):
        return Response(
            {"error": str(exc), "code": "EntityNotFoundError"},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, DomainError):
        return Response(
            {"error": "Error de negocio", "detail": str(exc), "code": "DomainError"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # For any other unhandled exception, return the default response if one exists
    return response
