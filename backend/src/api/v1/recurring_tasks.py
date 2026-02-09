"""
Recurring Tasks API endpoints for the Todo application with advanced features.

This module provides API endpoints for recurring task pattern operations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...database import get_session
from ...models.recurring_task import RecurringTaskPattern
from ...models.user import User
from ...services.recurring_task_service import create_recurring_pattern, get_recurring_pattern, generate_recurring_tasks
from .models import RecurringPatternCreate, RecurringPatternResponse
from ..dependencies import get_current_user


router = APIRouter()


@router.post("/", response_model=RecurringPatternResponse)
def create_new_recurring_pattern(
    pattern_create: RecurringPatternCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new recurring task pattern that will generate tasks automatically.
    """
    pattern_data = pattern_create.model_dump()

    pattern = create_recurring_pattern(
        session=session,
        pattern_data=pattern_data,
        user_id=current_user.id
    )

    if not pattern:
        raise HTTPException(status_code=400, detail="Invalid pattern data")

    # Convert to response model
    return RecurringPatternResponse(
        id=str(pattern.id),
        user_id=str(pattern.user_id),
        frequency=pattern.frequency,
        interval=pattern.interval,
        end_condition_type=pattern.end_condition_type,
        end_after_count=pattern.end_after_count,
        end_date=pattern.end_date,
        weekdays_mask=pattern.weekdays_mask,
        day_of_month=pattern.day_of_month,
        created_at=pattern.created_at,
        updated_at=pattern.updated_at
    )


@router.get("/{pattern_id}", response_model=RecurringPatternResponse)
def read_recurring_pattern(
    pattern_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific recurring pattern by ID.
    """
    pattern = get_recurring_pattern(
        session=session,
        pattern_id=pattern_id,
        user_id=current_user.id
    )

    if not pattern:
        raise HTTPException(status_code=404, detail="Recurring pattern not found")

    # Convert to response model
    return RecurringPatternResponse(
        id=str(pattern.id),
        user_id=str(pattern.user_id),
        frequency=pattern.frequency,
        interval=pattern.interval,
        end_condition_type=pattern.end_condition_type,
        end_after_count=pattern.end_after_count,
        end_date=pattern.end_date,
        weekdays_mask=pattern.weekdays_mask,
        day_of_month=pattern.day_of_month,
        created_at=pattern.created_at,
        updated_at=pattern.updated_at
    )


@router.post("/generate/")
def generate_tasks_from_patterns(
    pattern_id: str,
    start_date: str,  # ISO format date string
    end_date: str,    # ISO format date string
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate tasks from a recurring pattern within a date range.
    """
    from datetime import datetime

    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")

    generated_tasks = generate_recurring_tasks(
        session=session,
        pattern_id=pattern_id,
        user_id=current_user.id,
        start_date=start_dt,
        end_date=end_dt
    )

    return {"generated_tasks": generated_tasks}