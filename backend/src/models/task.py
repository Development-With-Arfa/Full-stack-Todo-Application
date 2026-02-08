from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base model for Task with shared attributes."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(max_length=255)


class Task(TaskBase, table=True):
    """Task model representing a task in the database."""
    __tablename__ = "tasks"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(SQLModel):
    """Schema for creating a new task (user_id comes from JWT token)."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskList(SQLModel):
    """Schema for returning a list of tasks."""
    tasks: list[TaskRead]