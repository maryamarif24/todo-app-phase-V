"""
Task Event model for event-driven architecture.

This module implements event logging for task lifecycle events.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    pass  # No circular imports needed


class TaskEvent(SQLModel, table=True):
    """
    TaskEvent entity for event-driven architecture logging.

    Attributes:
        id: Unique event identifier (UUID)
        event_type: Type of event (TASK_CREATED, TASK_UPDATED, TASK_COMPLETED, REMINDER_TRIGGERED)
        task_id: Associated task (FK to tasks.id)
        payload: Event-specific data payload (JSONB)
        occurred_at: When event occurred
        processed: Whether event has been processed (default: False)
        processed_at: When event was processed (nullable)
    """

    __tablename__ = "task_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_type: str = Field(max_length=50)  # TASK_CREATED, TASK_UPDATED, TASK_COMPLETED, REMINDER_TRIGGERED
    task_id: uuid.UUID = Field(foreign_key="tasks.id", ondelete="CASCADE")
    payload: dict = Field(sa_column=Field(JSONB))  # Event-specific data
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)  # Whether event has been processed
    processed_at: Optional[datetime] = Field(default=None)  # When it was processed

    def __str__(self):
        return f"TaskEvent(id={self.id}, event_type={self.event_type}, task_id={self.task_id}, occurred_at={self.occurred_at})"