"""
Dapr package for the backend.

This package contains all Dapr integration components including:
- Pub/Sub abstractions
- Binding implementations for reminders
- Client wrapper for Dapr runtime interaction
"""

# Import all Dapr components to make them available at package level
try:
    from .pubsub import DaprPubSubClient
    from .bindings import DaprBindingsClient
    from .client import DaprRuntimeClient
except ImportError:
    # These modules will be created during implementation
    pass

__all__ = []

# Add Dapr components for Phase 5 if they exist
try:
    __all__.extend([
        "DaprPubSubClient",
        "DaprBindingsClient",
        "DaprRuntimeClient"
    ])
except NameError:
    pass