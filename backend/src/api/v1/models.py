"""
API models for the Todo application with advanced features.

This module provides Pydantic models for API requests and responses.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base model for task operations."""
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    due_date: Optional[datetime] = None
    completed: bool = False
    reminder_enabled: bool = False
    reminder_time: Optional[str] = None  # e.g., "1 day", "2 hours"


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    tags: Optional[List[str]] = []


class TaskUpdate(BaseModel):
    """Model for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None  # LOW, MEDIUM, HIGH
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    reminder_enabled: Optional[bool] = None
    reminder_time: Optional[str] = None  # e.g., "1 day", "2 hours"
    tags: Optional[List[str]] = None


class TaskResponse(TaskBase):
    """Model for task responses."""
    id: str
    user_id: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    recurrence_pattern_id: Optional[str] = None
    tags: List[str] = []


class RecurringPatternBase(BaseModel):
    """Base model for recurring task patterns."""
    frequency: str  # DAILY, WEEKLY, MONTHLY
    interval: int = 1  # Every 'interval' periods (e.g., every 2 weeks)
    end_condition_type: str = "NEVER"  # COUNT, DATE, NEVER
    end_after_count: Optional[int] = None
    end_date: Optional[datetime] = None
    weekdays_mask: Optional[int] = None  # For WEEKLY patterns (bitmask)
    day_of_month: Optional[int] = None  # For MONTHLY patterns


class RecurringPatternCreate(RecurringPatternBase):
    """Model for creating a recurring pattern."""
    pass


class RecurringPatternResponse(RecurringPatternBase):
    """Model for recurring pattern responses."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class SearchRequest(BaseModel):
    """Model for search requests."""
    query: str
    limit: int = 20
    filters: Optional[dict] = {}


class SearchResponse(BaseModel):
    """Model for search responses."""
    results: List[TaskResponse]
    total: int
    query: str
    took_ms: int