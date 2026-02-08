"""
User schemas for API response validation.
User creation is handled by Better Auth, so we only need response schemas.
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class UserResponseSchema(BaseModel):
    """Schema for user responses (read-only)."""

    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email address")
    is_active: bool = Field(default=True, description="User active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "is_active": True,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            ]
        }
    }
