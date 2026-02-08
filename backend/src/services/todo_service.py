"""
Todo service for database operations.

Optimized for Neon PostgreSQL with sync database operations.
"""

import uuid
from typing import List, Optional
from sqlmodel import select
from sqlmodel import Session
from datetime import datetime

from ..models import Todo, User


def get_todos_by_user(session: Session, user_id: uuid.UUID, completed: Optional[bool] = None) -> List[Todo]:
    """
    Retrieve all todos for a user.

    Args:
        session: Database session
        user_id: Owning user's UUID
        completed: Optional filter for completion status (True for completed, False for incomplete, None for all)

    Returns:
        List of Todo instances belonging to the user
    """
    statement = select(Todo).where(Todo.user_id == user_id)

    if completed is not None:
        statement = statement.where(Todo.is_complete == completed)

    statement = statement.order_by(Todo.created_at.desc())
    result = session.execute(statement)
    return list(result.scalars().all())


def get_todo_by_id(session: Session, todo_id: uuid.UUID) -> Optional[Todo]:
    """
    Retrieve a single todo by ID.

    Args:
        session: Database session
        todo_id: Todo's UUID

    Returns:
        Todo instance if found, None otherwise
    """
    statement = select(Todo).where(Todo.id == todo_id)
    result = session.execute(statement)
    return result.scalar_one_or_none()


def create_todo(
    session: Session,
    user_id: uuid.UUID,
    title: str,
    description: Optional[str] = None,
    priority: str = "MEDIUM",
    due_date: Optional[datetime] = None,
    reminder_enabled: bool = False,
    reminder_time: Optional[str] = None
) -> Todo:
    """
    Create a new todo for a user with advanced features.

    Args:
        session: Database session
        user_id: Owning user's UUID
        title: Todo title (1-255 chars)
        description: Optional todo description
        priority: Task priority level (LOW, MEDIUM, HIGH) - Default: MEDIUM
        due_date: Optional deadline for task completion
        reminder_enabled: Whether reminder notifications are enabled - Default: False
        reminder_time: Time before due_date to trigger reminder

    Returns:
        Created Todo instance
    """
    todo = Todo(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        reminder_enabled=reminder_enabled,
        reminder_time=reminder_time
    )
    return todo


def update_todo(
    session: Session,
    todo_id: uuid.UUID,
    title: Optional[str] = None,
    description: Optional[str] = None,
    is_complete: Optional[bool] = None,
    priority: Optional[str] = None,
    due_date: Optional[datetime] = None,
    reminder_enabled: Optional[bool] = None,
    reminder_time: Optional[str] = None
) -> Optional[Todo]:
    """
    Update an existing todo with advanced features.

    Args:
        session: Database session
        todo_id: Todo's UUID
        title: New title (optional)
        description: New description (optional)
        is_complete: New completion status (optional)
        priority: New priority level (optional)
        due_date: New due date (optional)
        reminder_enabled: New reminder enabled status (optional)
        reminder_time: New reminder time (optional)

    Returns:
        Updated Todo instance if found, None otherwise
    """
    todo = get_todo_by_id(session, todo_id)
    if todo is None:
        return None

    if title is not None:
        todo.title = title
    if description is not None:
        todo.description = description
    if is_complete is not None:
        todo.is_complete = is_complete
        # Update completed_at based on is_complete status
        if is_complete:
            todo.completed_at = datetime.utcnow()
        else:
            todo.completed_at = None
    elif is_complete is None and hasattr(todo, 'is_complete'):
        # If is_complete is not provided but todo was previously completed and is now incomplete
        pass  # Don't change completed_at

    # Update new advanced features
    if priority is not None:
        todo.priority = priority
    if due_date is not None:
        todo.due_date = due_date
    if reminder_enabled is not None:
        todo.reminder_enabled = reminder_enabled
    if reminder_time is not None:
        todo.reminder_time = reminder_time

    todo.updated_at = datetime.utcnow()
    return todo


def delete_todo(session: Session, todo_id: uuid.UUID) -> bool:
    """
    Delete a todo.

    Args:
        session: Database session
        todo_id: Todo's UUID

    Returns:
        True if deleted, False if not found
    """
    todo = get_todo_by_id(session, todo_id)
    if todo is None:
        return False

    session.delete(todo)
    return True


def toggle_todo_complete(session: Session, todo_id: uuid.UUID) -> Optional[Todo]:
    """
    Toggle the complete status of a todo.

    Args:
        session: Database session
        todo_id: Todo's UUID

    Returns:
        Updated Todo instance if found, None otherwise
    """
    todo = get_todo_by_id(session, todo_id)
    if todo is None:
        return None

    todo.is_complete = not todo.is_complete
    todo.updated_at = datetime.utcnow()

    # Update completed_at based on the new is_complete status
    if todo.is_complete:
        todo.completed_at = datetime.utcnow()
    else:
        todo.completed_at = None

    return todo


def get_todos_by_title(session: Session, user_id: uuid.UUID, title: str) -> List[Todo]:
    """
    Retrieve todos for a user by title (useful for natural language processing).

    Args:
        session: Database session
        user_id: User's UUID
        title: Title to search for

    Returns:
        List of matching Todo instances
    """
    statement = select(Todo).where(
        Todo.user_id == user_id,
        Todo.title.ilike(f"%{title}%")  # Case-insensitive partial match
    )
    result = session.execute(statement)
    return list(result.scalars().all())


def get_todo_by_title(session: Session, user_id: uuid.UUID, title: str) -> Optional[Todo]:
    """
    Retrieve a single todo by user and title (useful for natural language processing).

    Args:
        session: Database session
        user_id: User's UUID
        title: Exact title to search for

    Returns:
        Todo instance if found, None otherwise
    """
    statement = select(Todo).where(
        Todo.user_id == user_id,
        Todo.title == title
    )
    result = session.execute(statement)
    return result.scalar_one_or_none()


def verify_ownership(todo: Todo, user: User) -> bool:
    """
    Verify that a user owns a todo.

    Args:
        todo: Todo instance
        user: User instance

    Returns:
        True if user owns the todo, False otherwise
    """
    return todo.user_id == user.id
