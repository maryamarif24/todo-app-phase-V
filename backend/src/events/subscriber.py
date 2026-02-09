"""
Abstract Event Subscriber for the Todo application with event-driven architecture.

This module provides the interface for event subscription and handling.
"""

from abc import ABC, abstractmethod
from typing import Callable, Any, Dict


class EventSubscriber(ABC):
    """
    Abstract base class for event subscribers.

    Provides the interface for subscribing to and handling events in an event-driven architecture.
    """

    @abstractmethod
    async def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        """
        Subscribe to an event type with the given handler.

        Args:
            event_type: Type of event to subscribe to
            handler: Handler function to call when the event is received
        """
        pass

    @abstractmethod
    async def unsubscribe(self, event_type: str):
        """
        Unsubscribe from an event type.

        Args:
            event_type: Type of event to unsubscribe from
        """
        pass

    @abstractmethod
    async def start_listening(self):
        """
        Start listening for events.
        """
        pass

    @abstractmethod
    async def stop_listening(self):
        """
        Stop listening for events.
        """
        pass