"""
Tag model for task categorization and organization.

This module implements the tag functionality for categorizing tasks.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User  # Adjust import based on actual user model location
    from .task import Task


class Tag(SQLModel, table=True):
    """
    Tag entity for task categorization.

    Attributes:
        id: Unique tag identifier (UUID)
        name: Tag name (unique per user, 1-50 chars)
        user_id: User who created the tag (FK to users.id)
        color: Hex color code for tag display (e.g., '#FF5733')
        created_at: Creation timestamp
    """

    __tablename__ = "tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=50, index=True)  # Will be made unique per user via constraint
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    color: Optional[str] = Field(default="#3B82F6", max_length=7)  # Default blue color

    # Relationships
    user: "User" = Relationship(back_populates="tags")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return f"Tag(id={self.id}, name='{self.name}', user_id={self.user_id})"


# Many-to-Many relationship table
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