from typing import Generator, Dict, Any
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import logging
from contextlib import contextmanager


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPExceptionResponse(JSONResponse):
    """Custom HTTP Exception Response."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            content={"error": detail}
        )


def handle_error(status_code: int, detail: str):
    """Generic error handler."""
    logger.error(f"Error {status_code}: {detail}")
    return HTTPExceptionResponse(status_code=status_code, detail=detail)


def validate_user_access(requested_user_id: str, authenticated_user_id: str) -> bool:
    """Validate that the requested user matches the authenticated user."""
    return requested_user_id == authenticated_user_id


@contextmanager
def db_transaction(session):
    """Context manager for database transactions."""
    try:
        yield session
        # session.commit() would be called here in a real implementation
    except Exception as e:
        # session.rollback() would be called here in a real implementation
        raise e