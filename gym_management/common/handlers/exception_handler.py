from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException,
    InvalidInputException,
    PermissionDeniedException,
    DatabaseException
)

EXCEPTION_HANDLERS = {
    ResourceNotFoundException: (status.HTTP_404_NOT_FOUND, "Resource not found."),
    ValidationException: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Validation error."),
    UnauthorizedException: (status.HTTP_401_UNAUTHORIZED, "Unauthorized."),
    ForbiddenException: (status.HTTP_403_FORBIDDEN, "Forbidden."),
    ConflictException: (status.HTTP_409_CONFLICT, "Conflict."),
    InvalidInputException: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid input."),
    PermissionDeniedException: (status.HTTP_403_FORBIDDEN, "Permission denied."),
    DatabaseException: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Database error."),
}


def handle_exception(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        handler = EXCEPTION_HANDLERS.get(type(exc))
        if handler:
            status_code, detail = handler
            response = Response({'detail': detail}, status=status_code)
        else:
            response = Response(
                {'detail': 'An unexpected error occurred.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return response
