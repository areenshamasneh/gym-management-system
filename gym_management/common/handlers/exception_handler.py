from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

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
    if isinstance(exc, Http404):
        return Response({'detail': 'Resource not found.'}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, tuple(EXCEPTION_HANDLERS.keys())):
        status_code, detail = EXCEPTION_HANDLERS[type(exc)]
        return Response({'detail': detail}, status=status_code)

    response = exception_handler(exc, context)
    if response is not None:
        return response

    return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
