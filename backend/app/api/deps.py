from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_jwt_token, TokenPayload
from app.core.errors import ErrorMessages, raise_authentication_error

# OAuth2 scheme for automatic OpenAPI documentation
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenPayload:
    """
    Dependency to extract and verify JWT token from Authorization header.

    Usage:
        @app.get("/protected")
        async def protected_route(
            current_user: Annotated[TokenPayload, Depends(get_current_user)]
        ):
            user_id = current_user.sub
            return {"user_id": user_id}

    Args:
        credentials: Automatically extracted by HTTPBearer

    Returns:
        TokenPayload object with verified user information

    Raises:
        HTTPException: If authentication fails with user-friendly message
    """
    try:
        token = credentials.credentials
        return verify_jwt_token(token)
    except HTTPException:
        # Re-raise with improved error message
        raise_authentication_error(ErrorMessages.AUTH_INVALID)
    except Exception:
        # Catch any other errors and return generic auth error
        raise_authentication_error(ErrorMessages.AUTH_INVALID)


# Type alias for cleaner route signatures
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]
