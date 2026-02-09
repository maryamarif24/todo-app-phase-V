"""
Reminder service for the Todo application with advanced features.

This module provides functionality for task reminder management.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models.reminder import Reminder


def create_reminder(*, session: Session, task_id: str, scheduled_time: datetime) -> Optional[Reminder]:
    """
    Create a new reminder for a task.

    Args:
        session: Database session
        task_id: ID of the task to create a reminder for
        scheduled_time: When the reminder should be triggered

    Returns:
        The created Reminder object if successful
    """
    # Create the reminder object
    reminder = Reminder(
        task_id=task_id,
        scheduled_time=scheduled_time
    )

    # Add to database
    try:
        session.add(reminder)
        session.commit()
        session.refresh(reminder)
        return reminder
    except IntegrityError:
        session.rollback()
        return None


def schedule_reminder(*, session: Session, task_id: str, reminder_time_before_due: timedelta = None) -> Optional[Reminder]:
    """
    Schedule a reminder for a task based on its due date and the time before due date.

    Args:
        session: Database session
        task_id: ID of the task to schedule a reminder for
        reminder_time_before_due: Time before due date to trigger reminder (e.g., 1 day, 2 hours)

    Returns:
        The created Reminder object if successful
    """
    # For now, we'll just create a reminder for the task at a fixed time
    # In a real implementation, you'd need to retrieve the task's due date
    from ..models.task import Task
    task_statement = select(Task).where(Task.id == task_id)
    task = session.exec(task_statement).first()

    if not task or not task.due_date:
        return None

    # Calculate when the reminder should be triggered
    scheduled_time = task.due_date
    if reminder_time_before_due:
        scheduled_time = task.due_date - reminder_time_before_due

    return create_reminder(session=session, task_id=task_id, scheduled_time=scheduled_time)


def get_pending_reminders(*, session: Session, check_time: datetime = None) -> List[Reminder]:
    """
    Get all pending reminders that should be triggered.

    Args:
        session: Database session
        check_time: Time to check for pending reminders (defaults to now)

    Returns:
        List of pending Reminder objects
    """
    if check_time is None:
        check_time = datetime.utcnow()

    # Get all reminders scheduled before or at the check_time that haven't been sent yet
    statement = select(Reminder).where(
        Reminder.scheduled_time <= check_time,
        Reminder.sent == False
    )
    reminders = session.exec(statement).all()
    return reminders


def mark_reminder_as_sent(*, session: Session, reminder_id: str) -> bool:
    """
    Mark a reminder as sent.

    Args:
        session: Database session
        reminder_id: ID of the reminder to mark as sent

    Returns:
        True if successful, False otherwise
    """
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        return False

    reminder.sent = True
    reminder.sent_at = datetime.utcnow()
    reminder.delivery_attempts += 1

    try:
        session.add(reminder)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def mark_reminder_as_delivered(*, session: Session, reminder_id: str) -> bool:
    """
    Mark a reminder as delivered.

    Args:
        session: Database session
        reminder_id: ID of the reminder to mark as delivered

    Returns:
        True if successful, False otherwise
    """
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        return False

    reminder.delivered = True

    try:
        session.add(reminder)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False