"""
Recurring Task Pattern model for automated task generation.

This module implements recurring task functionality with flexible patterns.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User  # Adjust import based on actual user model location
    from .task import Task


class RecurringTaskPattern(SQLModel, table=True):
    """
    RecurringTaskPattern entity for defining recurring task templates.

    Attributes:
        id: Unique pattern identifier (UUID)
        user_id: User who created the pattern (FK to users.id)
        frequency: Recurrence frequency (DAILY, WEEKLY, MONTHLY)
        interval: Interval multiplier (e.g., every 2 weeks: interval=2, frequency=WEEKLY)
        end_condition_type: End condition type (COUNT, DATE, NEVER)
        end_after_count: Number of occurrences (for COUNT type)
        end_date: End date (for DATE type)
        weekdays_mask: Bitmask for days of week (for WEEKLY - 1=Mon, 2=Tue, etc.)
        day_of_month: Day of month (for MONTHLY - 1-31)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "recurring_task_patterns"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    frequency: str = Field(max_length=20)  # DAILY, WEEKLY, MONTHLY
    interval: int = Field(default=1, ge=1, le=365)  # 1-365
    end_condition_type: str = Field(max_length=20, default="NEVER")  # COUNT, DATE, NEVER
    end_after_count: Optional[int] = Field(default=None, ge=1, le=1000)
    end_date: Optional[datetime] = Field(default=None)
    weekdays_mask: Optional[int] = Field(default=None, ge=1, le=127)  # Bitmask for WEEKLY
    day_of_month: Optional[int] = Field(default=None, ge=1, le=31)  # For MONTHLY

    # Relationships
    user: "User" = Relationship(back_populates="recurring_patterns")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return f"RecurringTaskPattern(id={self.id}, user_id={self.user_id}, frequency={self.frequency})"