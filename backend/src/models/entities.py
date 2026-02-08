"""
SQLModel entities for the Todo application.

This module exports User and Todo models with proper relationships
for user-specific todo data isolation.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


# Import the User model from user.py instead of defining here
from .user import User


class Todo(SQLModel, table=True):
    """
    Todo entity representing a task owned by a user.

    Attributes:
        id: Unique todo identifier (UUID)
        user_id: Owning user identifier (FK to users.id)
        title: Todo title (required, 1-255 chars) - Extended to 255 chars
        description: Optional todo description (max 2000 chars)
        is_complete: Completion status (default false)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        completed_at: Timestamp when the todo was marked as complete (nullable)
        # Phase 5 Advanced Features
        priority: Task priority level (LOW, MEDIUM, HIGH) - Default: MEDIUM
        due_date: Optional deadline for task completion
        reminder_enabled: Whether reminder notifications are enabled - Default: False
        reminder_time: Time before due_date to trigger reminder (nullable)
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    title: str = Field(min_length=1, max_length=255)  # Extended from 200 to 255 chars
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Phase 5 Advanced Features
    priority: str = Field(default="MEDIUM", max_length=20)  # LOW, MEDIUM, HIGH
    due_date: Optional[datetime] = Field(default=None)
    reminder_enabled: bool = Field(default=False)
    reminder_time: Optional[str] = Field(default=None, max_length=20)  # e.g., "1 day", "2 hours"

    # Relationship to user
    user: User = Relationship(back_populates="todos")


# Re-export for convenience
__all__ = ["User", "Todo"]
