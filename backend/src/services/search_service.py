"""
Search service for the Todo application with advanced features.

This module provides search, filter, and sort functionality for tasks.
"""

from datetime import datetime
from typing import List, Dict, Any
from sqlmodel import Session, select
from sqlalchemy import or_, and_
from sqlalchemy.orm import selectinload
from ..models.task import Task


def search_tasks(*, session: Session, query: str, user_id: str) -> List[Task]:
    """
    Search tasks by title, description, or tags.

    Args:
        session: Database session
        query: Search query string
        user_id: ID of the user whose tasks to search

    Returns:
        List of tasks matching the search query
    """
    # Basic search in title and description
    statement = select(Task).where(
        Task.user_id == user_id,
        or_(
            Task.title.contains(query),
            Task.description.contains(query) if query else False
        )
    ).options(selectinload(Task.tags))

    tasks = session.exec(statement).all()
    return tasks


def filter_tasks(*, session: Session, user_id: str, filters: Dict[str, Any]) -> List[Task]:
    """
    Filter tasks based on provided criteria.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to filter
        filters: Dictionary of filter criteria

    Returns:
        List of tasks matching the filters
    """
    statement = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if filters.get('status'):
        status = filters['status']
        if status == 'pending':
            statement = statement.where(Task.completed == False)
        elif status == 'completed':
            statement = statement.where(Task.completed == True)

    # Apply priority filter
    if filters.get('priority'):
        priority = filters['priority']
        statement = statement.where(Task.priority == priority)

    # Apply tag filter
    if filters.get('tags'):
        tags = filters['tags']
        # This is simplified - in practice, you'd need to join with the TaskTag table
        # and check if any of the task's tags match those in the filter
        pass  # Placeholder for complex tag filtering

    # Apply date range filters
    if filters.get('due_date_start'):
        due_date_start = filters['due_date_start']
        statement = statement.where(Task.due_date >= due_date_start)

    if filters.get('due_date_end'):
        due_date_end = filters['due_date_end']
        statement = statement.where(Task.due_date <= due_date_end)

    tasks = session.exec(statement).all()
    return tasks


def sort_tasks(*, session: Session, user_id: str, sort_by: str = 'created_at', order: str = 'asc') -> List[Task]:
    """
    Sort tasks based on the specified criteria.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to sort
        sort_by: Field to sort by ('created_at', 'due_date', 'priority')
        order: Sort order ('asc' or 'desc')

    Returns:
        List of tasks sorted by the specified criteria
    """
    statement = select(Task).where(Task.user_id == user_id)

    # Apply sorting
    if sort_by == 'created_at':
        if order == 'desc':
            statement = statement.order_by(Task.created_at.desc())
        else:
            statement = statement.order_by(Task.created_at.asc())
    elif sort_by == 'due_date':
        if order == 'desc':
            statement = statement.order_by(Task.due_date.desc())
        else:
            statement = statement.order_by(Task.due_date.asc())
    elif sort_by == 'priority':
        # Priority ordering: HIGH, MEDIUM, LOW
        priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        if order == 'desc':
            # For descending, we want HIGH first, so we order by ascending priority_order value
            statement = statement.order_by(Task.priority.case(**priority_order).asc())
        else:
            # For ascending, we want LOW first, so we order by descending priority_order value
            statement = statement.order_by(Task.priority.case(**priority_order).desc())

    tasks = session.exec(statement).all()
    return tasks