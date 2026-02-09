"""
Tasks API endpoints for the Todo application with advanced features.

This module provides REST API endpoints for extended task operations.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime
from ...database import get_session
from ...models.entities import Todo as Task
from ...models.user import User
from ...services.todo_service import (
    get_todos_by_user, get_todo_by_id, create_todo, update_todo, delete_todo,
    toggle_todo_complete, verify_ownership
)
from .models import TaskCreate, TaskUpdate, TaskResponse
from ..dependencies import get_current_user


router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None, description="Filter by status (pending, completed)"),
    priority: Optional[str] = Query(None, description="Filter by priority (LOW, MEDIUM, HIGH)"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    due_date_start: Optional[str] = Query(None, description="Filter by due date start (ISO format)"),
    due_date_end: Optional[str] = Query(None, description="Filter by due date end (ISO format)"),
    sort_by: str = Query("created_at", description="Sort by field (created_at, due_date, priority)"),
    order: str = Query("asc", description="Sort order (asc, desc)"),
    limit: int = Query(20, ge=1, le=100, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get tasks with filtering, sorting, and pagination.
    """
    # Build query
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter
    if status:
        if status == "pending":
            query = query.where(Task.is_complete == False)
        elif status == "completed":
            query = query.where(Task.is_complete == True)

    # Apply priority filter
    if priority:
        query = query.where(Task.priority == priority)

    # Apply due date range filters
    if due_date_start:
        from datetime import datetime
        dt_start = datetime.fromisoformat(due_date_start.replace('Z', '+00:00'))
        query = query.where(Task.due_date >= dt_start)

    if due_date_end:
        from datetime import datetime
        dt_end = datetime.fromisoformat(due_date_end.replace('Z', '+00:00'))
        query = query.where(Task.due_date <= dt_end)

    # Apply sorting
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

    # Apply pagination
    query = query.offset(offset).limit(limit)

    tasks = session.exec(query).all()

    # Convert to response model
    response_tasks = []
    for task in tasks:
        response_tasks.append(TaskResponse(
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

    return response_tasks


@router.post("/", response_model=TaskResponse)
def create_new_task(
    task_create: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task with advanced features.
    """
    task = create_todo(
        session=session,
        user_id=current_user.id,
        title=task_create.title,
        description=task_create.description,
        priority=task_create.priority,
        due_date=task_create.due_date,
        reminder_enabled=task_create.reminder_enabled,
        reminder_time=task_create.reminder_time
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    # Convert to response model
    response_task = TaskResponse(
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
    )
    return response_task


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID.
    """
    import uuid
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = get_todo_by_id(session=session, todo_id=task_uuid)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Convert to response model
    response_task = TaskResponse(
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
    )
    return response_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task with new attributes including priority, due date, tags, etc.
    """
    import uuid
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = get_todo_by_id(session=session, todo_id=task_uuid)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    task = update_todo(
        session=session,
        todo_id=task_uuid,
        title=task_update.title,
        description=task_update.description,
        is_complete=task_update.completed,
        priority=task_update.priority,
        due_date=task_update.due_date,
        reminder_enabled=task_update.reminder_enabled,
        reminder_time=task_update.reminder_time
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    # Convert to response model
    response_task = TaskResponse(
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
    )
    return response_task


@router.delete("/{task_id}")
def delete_existing_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task from the system.
    """
    import uuid
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = get_todo_by_id(session=session, todo_id=task_uuid)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    success = delete_todo(session=session, todo_id=task_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    session.commit()
    return {"message": "Task deleted successfully"}