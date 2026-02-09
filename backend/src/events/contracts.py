"""
Event contracts for the Todo application with event-driven architecture.

This module defines the contract schemas for all events in the system.
"""

from datetime import datetime
from typing import Any, Dict, Optional
import uuid


class TaskEventContract:
    """
    Defines the contracts for task-related events in the system.
    """

    @staticmethod
    def validate_task_created_event(payload: Dict[str, Any]) -> bool:
        """
        Validate the payload for a TaskCreated event.

        Args:
            payload: Payload to validate

        Returns:
            True if the payload is valid, False otherwise
        """
        required_keys = {"task_id", "user_id", "priority", "timestamp"}
        return all(key in payload for key in required_keys)

    @staticmethod
    def validate_task_updated_event(payload: Dict[str, Any]) -> bool:
        """
        Validate the payload for a TaskUpdated event.

        Args:
            payload: Payload to validate

        Returns:
            True if the payload is valid, False otherwise
        """
        required_keys = {"task_id", "user_id", "updated_fields", "timestamp"}
        return all(key in payload for key in required_keys)

    @staticmethod
    def validate_task_completed_event(payload: Dict[str, Any]) -> bool:
        """
        Validate the payload for a TaskCompleted event.

        Args:
            payload: Payload to validate

        Returns:
            True if the payload is valid, False otherwise
        """
        required_keys = {"task_id", "user_id", "completed_at", "timestamp"}
        return all(key in payload for key in required_keys)

    @staticmethod
    def validate_reminder_triggered_event(payload: Dict[str, Any]) -> bool:
        """
        Validate the payload for a ReminderTriggered event.

        Args:
            payload: Payload to validate

        Returns:
            True if the payload is valid, False otherwise
        """
        required_keys = {"task_id", "user_id", "reminder_id", "timestamp"}
        return all(key in payload for key in required_keys)

    @staticmethod
    def validate_recurring_task_generated_event(payload: Dict[str, Any]) -> bool:
        """
        Validate the payload for a RecurringTaskGenerated event.

        Args:
            payload: Payload to validate

        Returns:
            True if the payload is valid, False otherwise
        """
        required_keys = {"new_task_id", "original_task_id", "user_id", "generated_for_date", "recurrence_pattern", "timestamp"}
        return all(key in payload for key in required_keys)

    @staticmethod
    def create_task_created_contract(task_id: str, user_id: str, priority: str = "MEDIUM") -> Dict[str, Any]:
        """
        Create a properly structured TaskCreated event contract.

        Args:
            task_id: ID of the created task
            user_id: ID of the user who created the task
            priority: Priority level of the task

        Returns:
            Structured event payload
        """
        return {
            "event_id": str(uuid.uuid4()),
            "task_id": task_id,
            "user_id": user_id,
            "priority": priority,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "priority": priority
            }
        }

    @staticmethod
    def create_task_updated_contract(task_id: str, user_id: str, updated_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a properly structured TaskUpdated event contract.

        Args:
            task_id: ID of the updated task
            user_id: ID of the user who updated the task
            updated_fields: Dictionary of fields that were updated

        Returns:
            Structured event payload
        """
        return {
            "event_id": str(uuid.uuid4()),
            "task_id": task_id,
            "user_id": user_id,
            "updated_fields": updated_fields,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "updated_fields": updated_fields
            }
        }

    @staticmethod
    def create_task_completed_contract(task_id: str, user_id: str, completed_at: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Create a properly structured TaskCompleted event contract.

        Args:
            task_id: ID of the completed task
            user_id: ID of the user who completed the task
            completed_at: When the task was completed

        Returns:
            Structured event payload
        """
        completed_time = completed_at or datetime.utcnow()
        return {
            "event_id": str(uuid.uuid4()),
            "task_id": task_id,
            "user_id": user_id,
            "completed_at": completed_time.isoformat(),
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "completed_at": completed_time.isoformat()
            }
        }

    @staticmethod
    def create_reminder_triggered_contract(task_id: str, user_id: str, reminder_id: str) -> Dict[str, Any]:
        """
        Create a properly structured ReminderTriggered event contract.

        Args:
            task_id: ID of the task with the triggered reminder
            user_id: ID of the user associated with the task
            reminder_id: ID of the triggered reminder

        Returns:
            Structured event payload
        """
        return {
            "event_id": str(uuid.uuid4()),
            "task_id": task_id,
            "user_id": user_id,
            "reminder_id": reminder_id,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "reminder_id": reminder_id
            }
        }

    @staticmethod
    def create_recurring_task_generated_contract(new_task_id: str, original_task_id: str, user_id: str,
                                               recurrence_pattern: str) -> Dict[str, Any]:
        """
        Create a properly structured RecurringTaskGenerated event contract.

        Args:
            new_task_id: ID of the new generated task instance
            original_task_id: ID of the original recurring task template
            user_id: ID of the user who owns the task
            recurrence_pattern: Pattern of recurrence (DAILY, WEEKLY, MONTHLY)

        Returns:
            Structured event payload
        """
        return {
            "event_id": str(uuid.uuid4()),
            "new_task_id": new_task_id,
            "original_task_id": original_task_id,
            "user_id": user_id,
            "recurrence_pattern": recurrence_pattern,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "recurrence_pattern": recurrence_pattern
            }
        }