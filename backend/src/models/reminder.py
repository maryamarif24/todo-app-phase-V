"""
Reminder model for time-based task notifications.

This module implements reminder functionality for task deadlines and notifications.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .task import Task  # Adjust import based on actual task model location


class Reminder(SQLModel, table=True):
    """
    Reminder entity for time-based task notifications.

    Attributes:
        id: Unique reminder identifier (UUID)
        task_id: Associated task (FK to tasks.id)
        scheduled_time: When reminder should be triggered
        sent: Whether reminder has been sent (default: False)
        sent_at: When reminder was actually sent (nullable)
        delivered: Whether reminder was delivered successfully (default: False)
        delivery_attempts: Number of delivery attempts (default: 0)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "reminders"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="tasks.id", ondelete="CASCADE")
    scheduled_time: datetime = Field()  # When to trigger the reminder
    sent: bool = Field(default=False)  # Whether the reminder has been sent
    sent_at: Optional[datetime] = Field(default=None)  # When it was sent
    delivered: bool = Field(default=False)  # Whether it was delivered successfully
    delivery_attempts: int = Field(default=0, ge=0, le=5)  # Number of delivery attempts

    # Relationships
    task: "Task" = Relationship(back_populates="reminders")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return f"Reminder(id={self.id}, task_id={self.task_id}, scheduled_time={self.scheduled_time})"