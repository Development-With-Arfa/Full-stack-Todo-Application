from typing import Optional, List
from uuid import UUID
from sqlmodel import select, Session
from ..models.task import Task, TaskCreate, TaskUpdate
from datetime import datetime


def create_task(*, session: Session, task: TaskCreate, user_id: str) -> Task:
    """
    Create a new task in the database.

    Args:
        session: Database session
        task: TaskCreate object with task data
        user_id: ID of the user creating the task

    Returns:
        Task: The created task object
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_user_tasks(*, session: Session, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve

    Returns:
        List[Task]: List of tasks belonging to the user
    """
    statement = select(Task).where(Task.user_id == user_id)
    result = session.exec(statement)
    return result.all()


def get_task_by_id(*, session: Session, task_id: UUID, user_id: str) -> Optional[Task]:
    """
    Get a specific task by its ID for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user requesting the task

    Returns:
        Task or None: The task if found and belongs to the user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = session.exec(statement)
    return result.first()


def update_task(*, session: Session, task_id: UUID, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """
    Update a specific task by its ID for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to update
        task_update: TaskUpdate object with update data
        user_id: ID of the user updating the task

    Returns:
        Task or None: The updated task if found and belongs to the user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = session.exec(statement)
    db_task = result.first()

    if not db_task:
        return None

    # Update fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(*, session: Session, task_id: UUID, user_id: str) -> bool:
    """
    Delete a specific task by its ID for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user deleting the task

    Returns:
        bool: True if task was deleted, False if not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = session.exec(statement)
    db_task = result.first()

    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True