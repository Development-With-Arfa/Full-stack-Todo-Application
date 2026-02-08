from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Task(SQLModel, table=True):
    """Task model with user ownership."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})

    # Foreign key to users table
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        sa_column_kwargs={"nullable": False}
    )

    # Relationship to user
    owner: Optional["User"] = Relationship(back_populates="tasks")
