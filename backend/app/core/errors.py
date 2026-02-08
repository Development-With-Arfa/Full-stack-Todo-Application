"""
Custom error messages and exception handlers.
User-friendly messages that don't expose security details.
"""

from fastapi import HTTPException, status


class ErrorMessages:
    """Centralized error messages for consistent UX."""

    # Authentication errors (401)
    AUTH_REQUIRED = "Authentication required. Please sign in to continue."
    AUTH_INVALID = "Your session is invalid. Please sign in again."
    AUTH_EXPIRED = "Your session has expired. Please sign in again."
    TOKEN_MISSING = "Authentication token is missing. Please sign in."
    TOKEN_INVALID = "Authentication token is invalid. Please sign in again."

    # Authorization errors (403)
    FORBIDDEN = "You don't have permission to access this resource."
    TASK_NOT_OWNED = "You don't have permission to access this task."

    # Not found errors (404)
    TASK_NOT_FOUND = "Task not found. It may have been deleted."
    USER_NOT_FOUND = "User not found."

    # Validation errors (422)
    INVALID_INPUT = "The provided data is invalid. Please check your input."
    TITLE_REQUIRED = "Task title is required."
    TITLE_TOO_LONG = "Task title must be 255 characters or less."
    DESCRIPTION_TOO_LONG = "Task description must be 1000 characters or less."

    # Server errors (500)
    INTERNAL_ERROR = "An unexpected error occurred. Please try again later."
    DATABASE_ERROR = "A database error occurred. Please try again later."


def raise_authentication_error(detail: str = ErrorMessages.AUTH_INVALID):
    """Raise a 401 Unauthorized error."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_authorization_error(detail: str = ErrorMessages.FORBIDDEN):
    """Raise a 403 Forbidden error."""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


def raise_not_found_error(detail: str = ErrorMessages.TASK_NOT_FOUND):
    """Raise a 404 Not Found error."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )


def raise_validation_error(detail: str = ErrorMessages.INVALID_INPUT):
    """Raise a 422 Validation error."""
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail,
    )


def raise_internal_error(detail: str = ErrorMessages.INTERNAL_ERROR):
    """Raise a 500 Internal Server Error."""
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
    )
