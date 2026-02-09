"""
Events package for the backend.

This package contains all event-driven architecture components including:
- Publisher abstractions for Kafka/Dapr compatibility
- Subscriber handlers
- Event contracts and schemas
"""

# Import all event components to make them available at package level
try:
    from .publisher import EventPublisher
    from .subscriber import EventSubscriber
    from .kafka_publisher import KafkaEventPublisher
    from .dapr_publisher import DaprEventPublisher
    from .contracts import TaskEventContract
except ImportError:
    # These modules will be created during implementation
    pass

__all__ = []

# Add event components for Phase 5 if they exist
try:
    __all__.extend([
        "EventPublisher",
        "EventSubscriber",
        "KafkaEventPublisher",
        "DaprEventPublisher",
        "TaskEventContract"
    ])
except NameError:
    pass