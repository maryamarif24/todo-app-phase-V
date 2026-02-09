"""
Task service for the Todo application with advanced features.

This module provides CRUD operations for the extended Task model.
"""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


def create_task(*, session: Session, task_create: TaskCreate, user_id: str) -> Task:
    """
    Create a new task with the given data.

    Args:
        session: Database session
        task_create: Task creation data
        user_id: ID of the user creating the task

    Returns:
        The created Task object
    """
    # Create the task object
    task = Task.model_validate(task_create, update={"user_id": user_id})

    # Add to database
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_task_by_id(*, session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a task by its ID for the specified user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        The Task object if found and owned by the user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def update_task(*, session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """
    Update a task with the given data.

    Args:
        session: Database session
        task_id: ID of the task to update
        task_update: Task update data
        user_id: ID of the user who owns the task

    Returns:
        The updated Task object if successful, None if not found or not owned by user
    """
    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        return None

    # Update task with provided data
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(*, session: Session, task_id: str, user_id: str) -> bool:
    """
    Delete a task by its ID.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Returns:
        True if deletion was successful, False if task not found or not owned by user
    """
    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def get_tasks_with_filters(*, session: Session, user_id: str, status: Optional[str] = None,
                          priority: Optional[str] = None, tag: Optional[str] = None,
                          due_date_start: Optional[datetime] = None, due_date_end: Optional[datetime] = None) -> List[Task]:
    """
    Get tasks with optional filtering.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        status: Optional status filter (pending, completed)
        priority: Optional priority filter (LOW, MEDIUM, HIGH)
        tag: Optional tag filter
        due_date_start: Optional due date start filter
        due_date_end: Optional due date end filter

    Returns:
        List of tasks matching the filters
    """
    statement = select(Task).where(Task.user_id == user_id)

    if status:
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)

    if priority:
        statement = statement.where(Task.priority == priority)

    if due_date_start:
        statement = statement.where(Task.due_date >= due_date_start)

    if due_date_end:
        statement = statement.where(Task.due_date <= due_date_end)

    tasks = session.exec(statement).all()
    return tasks


def get_tasks_paginated(*, session: Session, user_id: str, limit: int = 20, offset: int = 0) -> List[Task]:
    """
    Get tasks with pagination.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip

    Returns:
        List of tasks for the given page
    """
    statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
    tasks = session.exec(statement).all()
    return tasks