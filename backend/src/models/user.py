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
    from .entities import Todo  # Only import what's definitely available


class User(SQLModel, table=True):
    """
    User entity representing an authenticated user.

    Attributes:
        id: Unique user identifier (UUID)
        email: User's email address (unique, indexed)
        password_hash: Hashed password (bcrypt output, min 60 chars)
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = 'users'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(min_length=60)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships to entities (will be resolved after other models are defined)
    todos: List["Todo"] = Relationship(back_populates="user")
    # Phase 5 relationships are defined as string references to avoid circular imports
    tasks: List["Task"] = Relationship(back_populates="user")
    tags: List["Tag"] = Relationship(back_populates="user")
    recurring_patterns: List["RecurringTaskPattern"] = Relationship(back_populates="user")


# Re-export for convenience
__all__ = ["User"]
