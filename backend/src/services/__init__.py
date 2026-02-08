"""
Services module exports.

This module provides centralized exports for all service layer modules.
"""

from .user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_password,
    get_or_create_user,
)
from .todo_service import (
    get_todos_by_user,
    get_todo_by_id,
    create_todo,
    update_todo,
    delete_todo,
    toggle_todo_complete,
    verify_ownership,
)

# Import new services for Phase 5 Advanced Features
try:
    from .task_service import (
        create_task,
        get_task_by_id,
        update_task,
        delete_task,
        get_tasks_with_filters,
        get_tasks_paginated,
    )
    from .tag_service import (
        create_tag,
        get_tag_by_name,
        get_tags_by_user,
        add_tag_to_task,
        remove_tag_from_task,
    )
    from .search_service import (
        search_tasks,
        filter_tasks,
        sort_tasks,
    )
    from .recurring_task_service import (
        create_recurring_pattern,
        get_recurring_pattern,
        generate_recurring_tasks,
    )
    from .reminder_service import (
        create_reminder,
        schedule_reminder,
        get_pending_reminders,
    )
    from .event_service import (
        emit_task_created_event,
        emit_task_updated_event,
        emit_task_completed_event,
        emit_reminder_triggered_event,
    )
except ImportError:
    # These services will be created during implementation
    pass

__all__ = [
    # User services
    "create_user",
    "get_user_by_email",
    "get_user_by_id",
    "verify_password",
    "get_or_create_user",
    # Todo services
    "get_todos_by_user",
    "get_todo_by_id",
    "create_todo",
    "update_todo",
    "delete_todo",
    "toggle_todo_complete",
    "verify_ownership",
]

# Add new services for Phase 5 if they exist
try:
    __all__.extend([
        # Task services
        "create_task",
        "get_task_by_id",
        "update_task",
        "delete_task",
        "get_tasks_with_filters",
        "get_tasks_paginated",
        # Tag services
        "create_tag",
        "get_tag_by_name",
        "get_tags_by_user",
        "add_tag_to_task",
        "remove_tag_from_task",
        # Search services
        "search_tasks",
        "filter_tasks",
        "sort_tasks",
        # Recurring task services
        "create_recurring_pattern",
        "get_recurring_pattern",
        "generate_recurring_tasks",
        # Reminder services
        "create_reminder",
        "schedule_reminder",
        "get_pending_reminders",
        # Event services
        "emit_task_created_event",
        "emit_task_updated_event",
        "emit_task_completed_event",
        "emit_reminder_triggered_event",
    ])
except NameError:
    pass
