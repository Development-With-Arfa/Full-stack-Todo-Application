import os
from typing import Optional
import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, status
from pydantic import BaseModel

# Configuration from environment
JWKS_URL = os.getenv("BETTER_AUTH_JWKS_URL", "http://localhost:3000/api/auth/jwks")
ISSUER = os.getenv("BETTER_AUTH_ISSUER", "http://localhost:3000")
AUDIENCE = os.getenv("BETTER_AUTH_AUDIENCE", "http://localhost:3000")
ALGORITHM = "EdDSA"  # Better Auth default

# Initialize JWKS client (caches keys automatically)
jwks_client = PyJWKClient(JWKS_URL)


class TokenPayload(BaseModel):
    sub: str  # User ID
    email: Optional[str] = None
    exp: int
    iss: str
    aud: str


def verify_jwt_token(token: str) -> TokenPayload:
    """
    Verify JWT token using JWKS endpoint.

    Args:
        token: JWT token string

    Returns:
        TokenPayload with user information

    Raises:
        HTTPException: If token is invalid, expired, or verification fails
    """
    try:
        # Get signing key from JWKS endpoint (cached)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Decode and verify token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
                "require": ["exp", "iss", "aud", "sub"]
            }
        )

        return TokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
