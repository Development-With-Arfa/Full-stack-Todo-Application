"""
Authentication-related Pydantic schemas.
"""

from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    """JWT token payload schema."""
    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    iss: str = Field(..., description="Issuer")
    aud: str = Field(..., description="Audience")
