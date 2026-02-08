from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import sys
import os

# Add the src directory to the path so imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))

from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from src.database.engine import get_sync_session
from src.services.task_service import (
    create_task as service_create_task,
    get_user_tasks as service_get_user_tasks,
    get_task_by_id as service_get_task_by_id,
    update_task as service_update_task,
    delete_task as service_delete_task
)

# Import authentication dependency and error handlers from app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../app"))
from app.api.deps import CurrentUser
from app.core.errors import (
    ErrorMessages,
    raise_not_found_error,
    raise_authorization_error,
    raise_internal_error
)

router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    current_user: CurrentUser,
    session: Session = Depends(get_sync_session)
):
    """
    Get all tasks for the authenticated user.
    Requires valid JWT token in Authorization header.
    """
    try:
        # Extract user_id from verified JWT token (secure)
        user_id = current_user.sub
        tasks = service_get_user_tasks(session=session, user_id=user_id)
        return tasks
    except Exception as e:
        raise_internal_error(ErrorMessages.DATABASE_ERROR)


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: CurrentUser,
    session: Session = Depends(get_sync_session)
):
    """
    Create a new task for the authenticated user.
    Requires valid JWT token in Authorization header.
    """
    try:
        # Extract user_id from verified JWT token (secure)
        user_id = current_user.sub
        db_task = service_create_task(session=session, task=task, user_id=user_id)
        return db_task
    except Exception as e:
        print(f"ERROR creating task: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise_internal_error(ErrorMessages.DATABASE_ERROR)


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_sync_session)
):
    """
    Get a specific task by ID (ownership verified).
    Requires valid JWT token in Authorization header.
    Returns 403 Forbidden if task belongs to another user.
    """
    try:
        # Extract user_id from verified JWT token (secure)
        user_id = current_user.sub
        db_task = service_get_task_by_id(session=session, task_id=task_id, user_id=user_id)

        if not db_task:
            raise_not_found_error(ErrorMessages.TASK_NOT_FOUND)

        # Verify ownership
        if str(db_task.user_id) != user_id:
            raise_authorization_error(ErrorMessages.TASK_NOT_OWNED)

        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise_internal_error(ErrorMessages.DATABASE_ERROR)


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_sync_session)
):
    """
    Update a specific task by ID (ownership verified).
    Requires valid JWT token in Authorization header.
    Returns 403 Forbidden if task belongs to another user.
    """
    try:
        # Extract user_id from verified JWT token (secure)
        user_id = current_user.sub

        # First, get the task to verify ownership
        db_task = service_get_task_by_id(session=session, task_id=task_id, user_id=user_id)

        if not db_task:
            raise_not_found_error(ErrorMessages.TASK_NOT_FOUND)

        # Verify ownership
        if str(db_task.user_id) != user_id:
            raise_authorization_error(ErrorMessages.TASK_NOT_OWNED)

        # Update the task
        updated_task = service_update_task(
            session=session,
            task_id=task_id,
            task_update=task_update,
            user_id=user_id
        )

        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise_internal_error(ErrorMessages.DATABASE_ERROR)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_sync_session)
):
    """
    Delete a specific task by ID (ownership verified).
    Requires valid JWT token in Authorization header.
    Returns 403 Forbidden if task belongs to another user.
    """
    try:
        # Extract user_id from verified JWT token (secure)
        user_id = current_user.sub

        # First, get the task to verify ownership
        db_task = service_get_task_by_id(session=session, task_id=task_id, user_id=user_id)

        if not db_task:
            raise_not_found_error(ErrorMessages.TASK_NOT_FOUND)

        # Verify ownership
        if str(db_task.user_id) != user_id:
            raise_authorization_error(ErrorMessages.TASK_NOT_OWNED)

        # Delete the task
        deleted = service_delete_task(session=session, task_id=task_id, user_id=user_id)

        return  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        raise_internal_error(ErrorMessages.DATABASE_ERROR)
