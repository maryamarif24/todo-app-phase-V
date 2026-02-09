"""
Search API endpoints for the Todo application with advanced features.

This module provides API endpoints for task search, filtering, and sorting.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ...database import get_session
from ...models.entities import Todo as Task
from ...models.user import User
from .models import SearchRequest, SearchResponse, TaskResponse
from ..dependencies import get_current_user


router = APIRouter()


@router.post("/tasks", response_model=SearchResponse)
def search_and_filter_tasks(
    search_request: SearchRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Search for tasks by title, description, or tags with additional filtering.
    """
    start_time = datetime.utcnow()

    # Build the query
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply search query if provided
    if search_request.query:
        search_term = f"%{search_request.query}%"
        query = query.where(
            Task.title.ilike(search_term) |
            Task.description.ilike(search_term)
        )

    # Apply filters from the request
    if search_request.filters:
        filters = search_request.filters
        if filters.get('status'):
            status = filters['status']
            if status == 'pending':
                query = query.where(Task.is_complete == False)
            elif status == 'completed':
                query = query.where(Task.is_complete == True)

        if filters.get('priority'):
            query = query.where(Task.priority == filters['priority'])

        if filters.get('due_date_start'):
            from datetime import datetime as dt
            due_date_start = dt.fromisoformat(filters['due_date_start'].replace('Z', '+00:00'))
            query = query.where(Task.due_date >= due_date_start)

        if filters.get('due_date_end'):
            from datetime import datetime as dt
            due_date_end = dt.fromisoformat(filters['due_date_end'].replace('Z', '+00:00'))
            query = query.where(Task.due_date <= due_date_end)

    # Apply sorting
    sort_by = 'created_at'
    order = 'asc'
    if search_request.filters:
        filters = search_request.filters
        sort_by = filters.get('sort_by', 'created_at')
        order = filters.get('order', 'asc')

    if sort_by == "created_at":
        if order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())
    elif sort_by == "due_date":
        if order == "desc":
            query = query.order_by(Task.due_date.desc())
        else:
            query = query.order_by(Task.due_date.asc())
    elif sort_by == "priority":
        # Priority ordering: HIGH, MEDIUM, LOW
        priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        if order == "desc":
            # For descending, we want HIGH first
            from sqlalchemy import case
            query = query.order_by(case(value=Task.priority, whens=priority_order).asc())
        else:
            # For ascending, we want LOW first
            from sqlalchemy import case
            query = query.order_by(case(value=Task.priority, whens=priority_order).desc())

    # Execute query
    results = session.exec(query).all()

    # Apply limit after retrieving all results
    limit = search_request.limit
    results = results[:limit]

    # Calculate elapsed time
    end_time = datetime.utcnow()
    took_ms = int((end_time - start_time).total_seconds() * 1000)

    # Convert results to response format
    response_results = []
    for task in results:
        response_results.append(TaskResponse(
            id=str(task.id),
            user_id=str(task.user_id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            completed=task.is_complete,
            completed_at=task.completed_at,
            reminder_enabled=task.reminder_enabled,
            reminder_time=task.reminder_time,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))

    # Format the response
    response = SearchResponse(
        results=response_results,
        total=len(response_results),
        query=search_request.query,
        took_ms=took_ms
    )

    return response