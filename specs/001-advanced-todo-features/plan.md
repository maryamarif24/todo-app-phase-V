# Implementation Plan: Advanced Features for Phase 5 (Part A)

**Branch**: `001-advanced-todo-features` | **Date**: 2026-02-05 | **Spec**: specs/001-advanced-todo-features/spec.md
**Input**: Feature specification from `/specs/001-advanced-todo-features/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of Phase 5 Advanced Features including enhanced task management (priority levels, due dates, tags), recurring tasks, time-based reminders, event-driven architecture with Kafka-compatible messaging, Dapr-ready abstractions, and professional frontend UX with home page and navigation. The plan encompasses backend data model updates, API extensions, event layer design, and frontend updates while maintaining backward compatibility with existing authentication flow.

## Technical Context

**Language/Version**: Python 3.11, TypeScript 5.0, Next.js 14.x
**Primary Dependencies**: FastAPI, SQLModel, Neon DB, Better Auth, React, Tailwind CSS
**Storage**: Neon DB (PostgreSQL) - existing database with schema extensions
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (browser-based), Linux/Mac/Windows compatible
**Project Type**: Web application (full-stack with frontend and backend)
**Performance Goals**: <2s page load time, <500ms API response time, 5000+ tasks per user searchable in <2s
**Constraints**: Must maintain backward compatibility with existing auth, follow event-driven architecture patterns, Dapr-ready abstractions
**Scale/Scope**: Support 10k+ concurrent users, handle complex search/filter operations efficiently

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Spec-Driven Development Compliance**: ✅ All code will be generated from approved specifications
**Agent Behavior Rules**: ✅ Implementation will follow spec exactly without invention
**Phase Governance**: ✅ Feature scope is within Phase V capabilities (event streaming, Dapr compatibility are approved)
**Quality Principles**: ✅ Plan includes clean architecture, event-driven patterns, Dapr-ready design, professional UX
**Technology Constraints**: ✅ All technologies comply with approved stack (Python, FastAPI, SQLModel, Neon DB, Next.js)
**Architectural Patterns**: ✅ Plan incorporates permitted patterns (event-driven, CQRS, Dapr building blocks)

## Project Structure

### Documentation (this feature)

```text
specs/001-advanced-todo-features/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py              # Extended task model with priority, due_date, tags, etc.
│   │   ├── recurring_task.py    # Recurring task pattern model
│   │   ├── reminder.py          # Reminder model
│   │   └── tag.py               # Tag/label model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py      # Enhanced task operations
│   │   ├── recurring_task_service.py  # Recurring task management
│   │   ├── reminder_service.py  # Reminder scheduling and triggers
│   │   ├── event_service.py     # Event emission and handling
│   │   └── search_service.py    # Search, filter, sort functionality
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py         # Extended task endpoints
│   │   │   ├── recurring_tasks.py  # Recurring task endpoints
│   │   │   └── search.py        # Search/filter endpoints
│   │   └── deps.py              # Dependency injection
│   ├── events/
│   │   ├── __init__.py
│   │   ├── publisher.py         # Event publishing abstraction
│   │   ├── subscriber.py        # Event subscription handler
│   │   ├── kafka_publisher.py   # Kafka-compatible event publisher
│   │   └── dapr_publisher.py    # Dapr-compatible event publisher
│   ├── dapr/
│   │   ├── __init__.py
│   │   ├── pubsub.py            # Dapr pub/sub abstraction
│   │   ├── bindings.py          # Dapr bindings for reminders
│   │   └── client.py            # Dapr runtime client
│   └── main.py                  # Application entry point
└── tests/
    ├── unit/
    │   ├── test_tasks.py        # Unit tests for task operations
    │   ├── test_recurring_tasks.py  # Unit tests for recurring tasks
    │   └── test_events.py       # Unit tests for event system
    ├── integration/
    │   ├── test_task_endpoints.py   # Integration tests for task API
    │   └── test_event_flow.py       # Integration tests for event flow
    └── contract/
        └── test_api_contracts.py    # Contract tests for API compliance

frontend/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── Navbar.tsx           # Professional navigation bar
│   │   ├── TaskForm.tsx         # Enhanced task creation form
│   │   ├── TaskList.tsx         # Task listing with filters/sort
│   │   ├── HomePage.tsx         # Public home page component
│   │   ├── ReminderModal.tsx    # Reminder notification component
│   │   └── TaskFilters.tsx      # Search, filter, sort controls
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── index.tsx            # Home page route
│   │   ├── dashboard.tsx        # Main dashboard with tasks
│   │   └── login.tsx            # Login page (existing)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api.ts               # API client for extended endpoints
│   │   ├── event_bus.ts         # Client-side event handling
│   │   └── reminder_handler.ts  # Client-side reminder management
│   ├── types/
│   │   ├── __init__.py
│   │   ├── task.ts              # Task type definitions
│   │   ├── recurring_task.ts    # Recurring task types
│   │   └── event.ts             # Event type definitions
│   └── utils/
│       ├── __init__.py
│       ├── date_utils.ts        # Date/time utility functions
│       └── search_utils.ts      # Search/filter utility functions
└── tests/
    ├── unit/
    │   ├── components/
    │   │   ├── TaskForm.test.tsx
    │   │   └── TaskList.test.tsx
    │   └── services/
    │       └── api.test.ts
    └── integration/
        └── pages/
            └── dashboard.test.tsx

contracts/
├── task-api-openapi.yaml         # OpenAPI spec for task endpoints
├── recurring-task-api-openapi.yaml  # OpenAPI spec for recurring tasks
└── event-contracts.json          # Event schema definitions
```

**Structure Decision**: Following the web application structure with separate backend and frontend directories to maintain clear separation of concerns while enabling event-driven communication and Dapr compatibility.

## Phase 0: Research & Unknown Resolution

### 0.1 Architecture Research
- Research Kafka-compatible event streaming implementations for Python/Next.js
- Investigate Dapr pub/sub and bindings patterns for reminder functionality
- Analyze search/filter performance optimizations for PostgreSQL

### 0.2 Technology Integration Patterns
- Best practices for integrating event-driven architecture with existing CRUD operations
- Dapr abstraction layer design to maintain compatibility without direct dependencies
- Client-side reminder synchronization with server-side triggers

### 0.3 Data Model Research
- Optimal PostgreSQL schema changes for performance with enhanced task features
- Indexing strategies for search, filter, and sort operations
- Recurring task state management patterns

## Phase 1: Design & Contracts

### 1.1 Data Model Design
- Extend Task model with priority, due_date, tags relationships
- Create RecurringTaskPattern model with frequency and end conditions
- Design Reminder model with trigger times and notification preferences
- Define TaskEvent model for event-driven architecture

### 1.2 API Contract Design
- Design extended task endpoints supporting new attributes
- Create recurring task CRUD endpoints
- Define search/filter/sort API endpoints
- Document event contracts for TaskCreated, TaskUpdated, TaskCompleted, ReminderTriggered events

### 1.3 Event Architecture Design
- Design event publishing abstraction supporting Kafka/Dapr
- Create event schema for all required event types
- Define event handling patterns for decoupled architecture
- Plan event replay and durability mechanisms

### 1.4 Frontend Component Design
- Design professional navbar component with authentication flow
- Create home page layout and content structure
- Plan enhanced task forms with priority/tags/due date inputs
- Design search/filter/sort UI controls

## Phase 2: Implementation Strategy

### 2.1 Backend Implementation
- Implement extended data models with SQLModel
- Build task service with new functionality
- Create event publishing layer
- Implement recurring task scheduler
- Develop search/filter/sort service

### 2.2 API Implementation
- Extend task endpoints with new features
- Implement recurring task endpoints
- Build search/filter/sort endpoints
- Connect event emission to business operations

### 2.3 Frontend Implementation
- Build professional navbar component
- Create enhanced task forms
- Implement search/filter/sort UI
- Build home page with value proposition

### 2.4 Integration & Testing
- End-to-end testing of new features
- Performance testing of search/filter operations
- Event flow validation and reliability testing
- Authentication flow integration testing

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Event Streaming (Kafka) | Scalability and integration requirements for Phase V | Direct service communication would create tight coupling and hinder distributed architecture |
| Dapr Compatibility Layer | Future-proofing for distributed deployment | Hardcoding to specific event system would block Phase V migration |
| Complex Search/Filter Operations | User experience requirement for managing large task sets | Basic filtering would not meet SC-002 performance criteria |
