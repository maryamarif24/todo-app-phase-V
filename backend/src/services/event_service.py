"""
Event service for the Todo application with event-driven architecture.

This module provides functionality for emitting task-related events.
"""

from datetime import datetime
from typing import Any, Dict
import uuid
from sqlmodel import Session
from ..models.task_event import TaskEvent


def emit_task_created_event(*, session: Session, task_id: str, user_id: str, priority: str = None) -> TaskEvent:
    """
    Emit a TaskCreated event.

    Args:
        session: Database session
        task_id: ID of the created task
        user_id: ID of the user who created the task
        priority: Priority level of the task

    Returns:
        The created TaskEvent object
    """
    event_payload = {
        "task_id": task_id,
        "user_id": user_id,
        "priority": priority or "MEDIUM",
        "timestamp": datetime.utcnow().isoformat()
    }

    event = TaskEvent(
        event_type="TASK_CREATED",
        task_id=task_id,
        payload=event_payload,
        occurred_at=datetime.utcnow()
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


def emit_task_updated_event(*, session: Session, task_id: str, user_id: str, updated_fields: Dict[str, Any]) -> TaskEvent:
    """
    Emit a TaskUpdated event.

    Args:
        session: Database session
        task_id: ID of the updated task
        user_id: ID of the user who updated the task
        updated_fields: Dictionary of fields that were updated

    Returns:
        The created TaskEvent object
    """
    event_payload = {
        "task_id": task_id,
        "user_id": user_id,
        "updated_fields": updated_fields,
        "timestamp": datetime.utcnow().isoformat()
    }

    event = TaskEvent(
        event_type="TASK_UPDATED",
        task_id=task_id,
        payload=event_payload,
        occurred_at=datetime.utcnow()
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


def emit_task_completed_event(*, session: Session, task_id: str, user_id: str, completed_at: datetime = None) -> TaskEvent:
    """
    Emit a TaskCompleted event.

    Args:
        session: Database session
        task_id: ID of the completed task
        user_id: ID of the user who completed the task
        completed_at: When the task was completed

    Returns:
        The created TaskEvent object
    """
    event_payload = {
        "task_id": task_id,
        "user_id": user_id,
        "completed_at": (completed_at or datetime.utcnow()).isoformat(),
        "timestamp": datetime.utcnow().isoformat()
    }

    event = TaskEvent(
        event_type="TASK_COMPLETED",
        task_id=task_id,
        payload=event_payload,
        occurred_at=datetime.utcnow()
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


def emit_reminder_triggered_event(*, session: Session, task_id: str, user_id: str, reminder_id: str) -> TaskEvent:
    """
    Emit a ReminderTriggered event.

    Args:
        session: Database session
        task_id: ID of the task with the triggered reminder
        user_id: ID of the user associated with the task
        reminder_id: ID of the triggered reminder

    Returns:
        The created TaskEvent object
    """
    event_payload = {
        "task_id": task_id,
        "user_id": user_id,
        "reminder_id": reminder_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    event = TaskEvent(
        event_type="REMINDER_TRIGGERED",
        task_id=task_id,
        payload=event_payload,
        occurred_at=datetime.utcnow()
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event