"""
Recurring task service for the Todo application with advanced features.

This module provides CRUD operations for recurring task patterns and generation logic.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models.recurring_task import RecurringTaskPattern


def create_recurring_pattern(*, session: Session, pattern_data: dict, user_id: str) -> Optional[RecurringTaskPattern]:
    """
    Create a new recurring task pattern.

    Args:
        session: Database session
        pattern_data: Data for the recurring pattern
        user_id: ID of the user creating the pattern

    Returns:
        The created RecurringTaskPattern object if successful
    """
    # Create the pattern object
    pattern = RecurringTaskPattern(
        user_id=user_id,
        frequency=pattern_data.get('frequency'),
        interval=pattern_data.get('interval', 1),
        end_condition_type=pattern_data.get('end_condition_type', 'NEVER'),
        end_after_count=pattern_data.get('end_after_count'),
        end_date=pattern_data.get('end_date'),
        weekdays_mask=pattern_data.get('weekdays_mask'),
        day_of_month=pattern_data.get('day_of_month')
    )

    # Add to database
    try:
        session.add(pattern)
        session.commit()
        session.refresh(pattern)
        return pattern
    except IntegrityError:
        session.rollback()
        return None


def get_recurring_pattern(*, session: Session, pattern_id: str, user_id: str) -> Optional[RecurringTaskPattern]:
    """
    Get a recurring task pattern by its ID for the specified user.

    Args:
        session: Database session
        pattern_id: ID of the pattern to retrieve
        user_id: ID of the user who owns the pattern

    Returns:
        The RecurringTaskPattern object if found and owned by the user, None otherwise
    """
    statement = select(RecurringTaskPattern).where(
        RecurringTaskPattern.id == pattern_id,
        RecurringTaskPattern.user_id == user_id
    )
    pattern = session.exec(statement).first()
    return pattern


def generate_recurring_tasks(*, session: Session, pattern_id: str, user_id: str, start_date: datetime, end_date: datetime) -> List[dict]:
    """
    Generate tasks based on a recurring pattern within a date range.

    Args:
        session: Database session
        pattern_id: ID of the pattern to use for generation
        user_id: ID of the user whose pattern to use
        start_date: Start date for generation
        end_date: End date for generation

    Returns:
        List of task definitions that should be created
    """
    pattern = get_recurring_pattern(session=session, pattern_id=pattern_id, user_id=user_id)
    if not pattern:
        return []

    generated_tasks = []
    current_date = start_date

    while current_date <= end_date:
        # Check if current date fits the pattern
        should_generate = False

        if pattern.frequency == "DAILY":
            should_generate = True
            current_date = current_date + timedelta(days=pattern.interval)
        elif pattern.frequency == "WEEKLY":
            if pattern.weekdays_mask:
                # Check if current weekday is in the mask
                weekday_bit = 1 << current_date.weekday()  # Monday is 0
                if pattern.weekdays_mask & weekday_bit:
                    should_generate = True
            else:
                should_generate = True  # If no mask, generate on interval basis
            current_date = current_date + timedelta(weeks=pattern.interval)
        elif pattern.frequency == "MONTHLY":
            if pattern.day_of_month:
                # Generate on specific day of month
                if current_date.day == pattern.day_of_month:
                    should_generate = True
            else:
                # Generate on the same day of month as pattern creation
                should_generate = True
            # Advance by month(s) - be careful with different month lengths
            try:
                current_date = current_date.replace(month=current_date.month + pattern.interval)
            except ValueError:
                # Handle months with fewer days (e.g. Feb 31st -> Mar 3rd)
                import calendar
                max_day = calendar.monthrange(current_date.year, current_date.month + pattern.interval)[1]
                adjusted_day = min(current_date.day, max_day)
                current_date = current_date.replace(month=current_date.month + pattern.interval, day=adjusted_day)

        if should_generate:
            # Create task definition based on pattern
            task_definition = {
                'title': f'Recurring: Pattern {pattern_id}',
                'due_date': current_date,
                'pattern_id': pattern.id,
                'user_id': user_id
            }
            generated_tasks.append(task_definition)

        # Check end conditions
        if pattern.end_condition_type == 'DATE' and current_date > pattern.end_date:
            break

    return generated_tasks