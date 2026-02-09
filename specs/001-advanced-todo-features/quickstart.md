# Quickstart Guide: Advanced Features for Phase 5 (Part A)

**Date**: 2026-02-05
**Feature**: Advanced Features for Phase 5 (Part A)
**Branch**: 001-advanced-todo-features

## Overview

This quickstart guide provides essential information for developers to begin implementing the Phase 5 Advanced Features, including enhanced task management, event-driven architecture, and Dapr readiness.

## Prerequisites

### System Requirements
- Python 3.11+
- Node.js 18+ / npm 9+
- PostgreSQL (local development) or Neon DB account
- Docker Desktop (for containerized development)
- Dapr installed locally (optional for development)

### Development Setup
1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `npm install`
4. Configure environment variables (see .env.example)
5. Run database migrations: `alembic upgrade head`

## Key Architecture Components

### Backend Structure
```
backend/
├── src/
│   ├── models/           # Extended data models with advanced features
│   ├── services/         # Business logic and task management services
│   ├── api/              # REST API endpoints with new functionality
│   ├── events/           # Event publishing and handling layer
│   └── dapr/             # Dapr abstraction and integration layer
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # Reusable UI components (Navbar, TaskForm, etc.)
│   ├── pages/            # Route-specific pages (Home, Dashboard, etc.)
│   ├── services/         # API clients and event handling
│   └── types/            # TypeScript definitions for new features
```

## Environment Configuration

### Required Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/dbname

# Kafka Configuration (for event streaming)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ENABLE_EVENTS=false  # Set to true to enable event streaming

# Dapr Configuration
DAPR_ENABLED=false         # Set to true when Dapr is running
DAPR_PUBSUB_NAME=task-pubsub
DAPR_STATE_STORE_NAME=task-state

# Feature Flags
ENABLE_RECURRING_TASKS=true
ENABLE_ADVANCED_SEARCH=true
ENABLE_REMINDERS=true
```

## Running the Application

### Local Development
```bash
# Start backend (with hot reload)
cd backend
uvicorn src.main:app --reload --port 8000

# Start frontend (with hot reload)
cd frontend
npm run dev

# Start Dapr (if using Dapr features)
dapr run --app-id todo-app --app-port 8000 --dapr-http-port 3500 --dapr-grpc-port 50001
```

### With Docker Compose
```bash
docker-compose up --build
```

## Core Feature Workflows

### 1. Creating Enhanced Tasks
```python
# Backend: Create task with new attributes
task_service.create_task(
    user_id=user_id,
    title="Meeting preparation",
    priority="HIGH",
    due_date=datetime.now() + timedelta(days=2),
    tags=["work", "urgent"],
    reminder_enabled=True,
    reminder_time=timedelta(hours=1)
)
```

### 2. Event-Driven Architecture Pattern
```python
# Emit events when task operations occur
async def create_task(task_data):
    task = await task_repo.create(task_data)

    # Publish event asynchronously
    await event_publisher.publish("TaskCreated", {
        "task_id": task.id,
        "user_id": task.user_id,
        "timestamp": datetime.utcnow(),
        "priority": task.priority
    })

    return task
```

### 3. Dapr Integration (Conditional)
```python
# Abstract Dapr functionality
class TaskService:
    def __init__(self, event_publisher: EventPublisher):
        self.event_publisher = event_publisher  # Could be Kafka, Dapr, or mock

    async def publish_task_created(self, task_id: str, user_id: str):
        await self.event_publisher.publish("TaskCreated", {
            "task_id": task_id,
            "user_id": user_id
        })
```

### 4. Frontend Task Form Integration
```typescript
// Enhanced task form with priority and tags
interface EnhancedTaskFormProps {
  onSubmit: (taskData: {
    title: string;
    priority: 'LOW' | 'MEDIUM' | 'HIGH';
    dueDate?: Date;
    tags: string[];
    recurringPattern?: RecurringPattern;
    reminderEnabled: boolean;
  }) => void;
}
```

## API Endpoints

### Extended Task Endpoints
- `POST /api/v1/tasks` - Create task with advanced attributes
- `GET /api/v1/tasks/search` - Search, filter, sort tasks
- `POST /api/v1/tasks/recurring` - Create recurring task pattern
- `GET /api/v1/tasks/recurring/{pattern_id}` - Get recurring tasks

### Event-Related Endpoints
- `GET /api/v1/events/pending` - Get unprocessed events
- `POST /api/v1/events/process` - Process pending events

## Database Migrations

### Running Migrations
```bash
# Backend directory
cd backend
alembic revision --autogenerate -m "Add advanced task features"
alembic upgrade head
```

### Migration Files Location
```
backend/
├── alembic/
│   └── versions/         # Migration files
```

## Testing Strategy

### Backend Tests
```bash
# Run all backend tests
cd backend
pytest tests/

# Run specific test suites
pytest tests/unit/test_tasks.py
pytest tests/integration/test_events.py
```

### Frontend Tests
```bash
# Run all frontend tests
cd frontend
npm run test

# Run specific test files
npm run test -- src/components/TaskForm.test.tsx
```

## Dapr Development

### Local Dapr Setup
1. Install Dapr CLI
2. Initialize Dapr: `dapr init`
3. Start with Dapr: `dapr run --app-id todo-app --app-port 8000 uvicorn src.main:app --host 0.0.0.0 --port 8000`

### Dapr Components
The application uses these Dapr building blocks:
- **Pub/Sub**: For event-driven communication
- **State Management**: For storing reminder schedules
- **Bindings**: For timer-based reminder triggers

## Troubleshooting

### Common Issues
1. **Event processing not working**: Check KAFKA_BOOTSTRAP_SERVERS configuration
2. **Dapr errors**: Ensure DAPR_ENABLED=true and dapr services are running
3. **Database connection errors**: Verify DATABASE_URL configuration
4. **Frontend API calls failing**: Confirm backend is running on expected port

### Debugging Events
- Check event logs: `docker logs todo-app-kafka` (for Kafka)
- Monitor Dapr: `dapr list` and `dapr status -a todo-app`
- Inspect event tables in database for processing status

## Deployment Notes

### Production Configuration
- Set `ENVIRONMENT=production` to enable production-optimized settings
- Enable SSL for all API communications
- Configure proper secrets management
- Set up monitoring for event processing

### Scaling Considerations
- Event processing services may need to be scaled independently
- Database connections should be pooled appropriately
- Cache layers may be needed for search functionality at scale