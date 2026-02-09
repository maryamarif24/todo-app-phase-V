"""
TaskTag junction model for the many-to-many relationship between Task and Tag.

This module implements the many-to-many relationship between Task and Tag entities.
"""

from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .task import Task
    from .tag import Tag


class TaskTag(SQLModel, table=True):
    """
    Junction table for the many-to-many relationship between Task and Tag.

    Attributes:
        task_id: Reference to the Task (FK to tasks.id)
        tag_id: Reference to the Tag (FK to tags.id)
        assigned_at: When the tag was assigned to the task
    """

    __tablename__ = "task_tags"

    task_id: uuid.UUID = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tags.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return f"TaskTag(task_id={self.task_id}, tag_id={self.tag_id}, assigned_at={self.assigned_at})"