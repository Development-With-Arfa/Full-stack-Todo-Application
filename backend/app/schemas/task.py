"""
Task schemas for API request/response validation.
Provides additional validation beyond SQLModel.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title (required, 1-255 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Ensure title is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Task title cannot be empty or whitespace only")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from description."""
        if v:
            stripped = v.strip()
            return stripped if stripped else None
        return None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Complete project documentation",
                    "description": "Write comprehensive docs for the authentication system"
                }
            ]
        }
    }


class TaskUpdateSchema(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated task title (optional, 1-255 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Updated task description (optional, max 1000 characters)"
    )
    completed: Optional[bool] = Field(
        None,
        description="Task completion status (optional)"
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not just whitespace if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError("Task title cannot be empty or whitespace only")
            return v.strip()
        return None

    @field_validator("description")
    @classmethod
    def description_strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from description."""
        if v is not None:
            stripped = v.strip()
            return stripped if stripped else None
        return None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Updated task title",
                    "completed": True
                }
            ]
        }
    }


class TaskResponseSchema(BaseModel):
    """Schema for task responses."""

    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(..., description="Task completion status")
    user_id: int = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Complete project documentation",
                    "description": "Write comprehensive docs for the authentication system",
                    "completed": False,
                    "user_id": 1,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            ]
        }
    }
