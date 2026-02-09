"""
Abstract Event Publisher for the Todo application with event-driven architecture.

This module provides the interface for event publishing with Kafka/Dapr compatibility.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class EventPublisher(ABC):
    """
    Abstract base class for event publishers.

    Provides the interface for publishing events in an event-driven architecture.
    """

    @abstractmethod
    async def publish(self, event_type: str, payload: Dict[str, Any]) -> bool:
        """
        Publish an event with the given type and payload.

        Args:
            event_type: Type of the event to publish
            payload: Event data payload

        Returns:
            True if the event was published successfully, False otherwise
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close the publisher and release any resources.
        """
        pass