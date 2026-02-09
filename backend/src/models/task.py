"""
Task model for the Todo application with extended features.

This module extends the existing Todo functionality with advanced features:
- Priority levels (LOW, MEDIUM, HIGH)
- Due dates for task deadlines
- Tags for categorization and organization
- Recurring task patterns
- Reminder functionality
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User  # Adjust import based on actual user model location
    from .tag import Tag
    from .recurring_task import RecurringTaskPattern
    from .reminder import Reminder


class Task(SQLModel, table=True):
    """
    Extended Task entity representing a task with advanced features.

    Attributes:
        id: Unique task identifier (UUID)
        user_id: Owning user identifier (FK to users.id)
        title: Task title (required, 1-255 chars)
        description: Optional task description (max 2000 chars)
        priority: Task priority level (LOW, MEDIUM, HIGH) - Default: MEDIUM
        due_date: Optional deadline for task completion
        completed: Completion status (default false)
        completed_at: Timestamp when the task was marked as completed (nullable)
        recurrence_pattern_id: FK to recurring pattern (nullable)
        reminder_enabled: Whether reminder notifications are enabled - Default: False
        reminder_time: Time before due_date to trigger reminder (nullable)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: str = Field(default="MEDIUM", max_length=20)  # LOW, MEDIUM, HIGH
    due_date: Optional[datetime] = Field(default=None)
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = Field(default=None)
    recurrence_pattern_id: Optional[uuid.UUID] = Field(default=None, foreign_key="recurring_task_patterns.id")
    reminder_enabled: bool = Field(default=False)
    reminder_time: Optional[str] = Field(default=None, max_length=20)  # e.g., "1 day", "2 hours"

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
    recurrence_pattern: Optional["RecurringTaskPattern"] = Relationship()
    reminders: List["Reminder"] = Relationship(back_populates="task")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation could be added here if needed
    def __str__(self):
        return f"Task(id={self.id}, title='{self.title}', user_id={self.user_id})"