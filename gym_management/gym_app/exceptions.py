from rest_framework.exceptions import APIException  # type: ignore


class ResourceNotFoundException(APIException):
    status_code = 404
    default_detail = "Resource not found."
    default_code = "resource_not_found"


class ValidationException(APIException):
    status_code = 422
    default_detail = "Validation error."
    default_code = "validation_error"


class UnauthorizedException(APIException):
    status_code = 401
    default_detail = "Unauthorized."
    default_code = "unauthorized"


class ForbiddenException(APIException):
    status_code = 403
    default_detail = "Forbidden."
    default_code = "forbidden"


class ConflictException(APIException):
    status_code = 409
    default_detail = "Conflict."
    default_code = "conflict"


class InvalidInputException(APIException):
    status_code = 422
    default_detail = "Invalid input."
    default_code = "invalid_input"


class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = "Permission denied."
    default_code = "permission_denied"


class DatabaseException(APIException):
    status_code = 500
    default_detail = "Database error."
    default_code = "database_error"
