"""
Database models module exports.

This module provides centralized exports for all SQLModel entities
and database utilities.
"""

from .database import (
    sync_engine,
    get_db,
    init_db,
    close_db,
    TimestampMixin,
)
from .entities import User, Todo
from .conversation import Conversation
from .message import Message

# Import new models for Phase 5 Advanced Features
# Using try/except to handle potential import issues during development
try:
    from .task import Task
    __all__ = [
        "sync_engine",
        "get_db",
        "init_db",
        "close_db",
        "TimestampMixin",
        "User",
        "Todo",
        "Conversation",
        "Message",
        "Task",
    ]

    # Import other models only after Task is successfully imported
    try:
        from .tag import Tag
        __all__.append("Tag")
    except:
        pass

    try:
        from .recurring_task import RecurringTaskPattern
        __all__.append("RecurringTaskPattern")
    except:
        pass

    try:
        from .reminder import Reminder
        __all__.append("Reminder")
    except:
        pass

    try:
        from .task_event import TaskEvent
        __all__.append("TaskEvent")
    except:
        pass

    try:
        from .task_tag import TaskTag
        __all__.append("TaskTag")
    except:
        pass

except ImportError:
    # If there's an issue importing Task, just export the original models
    __all__ = [
        "sync_engine",
        "get_db",
        "init_db",
        "close_db",
        "TimestampMixin",
        "User",
        "Todo",
        "Conversation",
        "Message",
    ]
