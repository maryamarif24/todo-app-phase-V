<!--
Sync Impact Report:
- Version change: 2.2.0 → 2.3.0
- Modified principles: None
- Added sections: New event-driven architecture principles, enhanced UX principles, Dapr-readiness requirements
- Removed sections: None
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md (updated for event-driven architecture)
  ✅ .specify/templates/spec-template.md (updated for advanced features)
  ✅ .specify/templates/tasks-template.md (updated for event-driven tasks)
- Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All code MUST be generated from approved specifications. NO manual coding by humans is permitted. The development flow is strictly: **Constitution → Specs → Plan → Tasks → Implement**. Code written without corresponding spec and task artifacts is invalid and MUST be rejected.

**Rationale**: Ensures traceability, prevents ad-hoc decisions, and maintains alignment between requirements and implementation. Spec-driven discipline is the foundation of multi-phase development.

### II. Agent Behavior Rules (NON-NEGOTIABLE)
All agents MUST adhere to strict behavior constraints:

1. **No Manual Coding**: Humans DO NOT write code directly. Humans define requirements, review artifacts, and approve implementations only.
2. **No Feature Invention**: Agents MUST NOT invent features, requirements, or capabilities not in approved specs.
3. **No Deviation**: Agents MUST implement specs exactly as written. Deviation without spec amendment is invalid.
4. **Spec-Level Refinement**: Any requirement clarification or refinement MUST occur at spec level, not during implementation.

**Rationale**: Uncontrolled agent behavior undermines multi-phase stability. Clear boundaries prevent scope drift and maintain architectural integrity across phases.

### III. Phase Governance (NON-NEGOTIABLE)
Each phase is strictly scoped by its specification:

1. **Phase Boundaries**: Each phase (I-V) has a defined scope. Features from future phases MUST NEVER leak into earlier phases.
2. **Phase-First Design**: Architecture evolves phase-by-phase through updated specs and plans. No anticipatory coding for future phases.
3. **Scope Locking**: Once a phase spec is approved, its scope is locked. Changes require formal amendment through spec revision.

**Rationale**: Phased evolution requires strict boundaries. Feature creep into earlier phases destabilizes development and creates technical debt.

### IV. Quality Principles (NON-NEGOTIABLE)
All code and architecture MUST adhere to quality standards:

1. **Clean Architecture**: Separation of concerns, no tight coupling, clear boundaries between layers.
2. **Stateless Services**: Services MUST be stateless where required (especially for cloud deployment). State is managed explicitly.
3. **Separation of Concerns**: Each module, function, or service has a single, well-defined responsibility.
4. **Cloud-Native Readiness**: Architecture is designed for cloud deployment from the beginning (even in early phases).
5. **Stateless MCP Tools**: MCP tools MUST NOT store in-memory state and MUST rely on database persistence for all state management.
6. **Agent-Database Interaction**: AI agents MAY ONLY interact with the system via MCP tools; direct database access is prohibited.
7. **Event-Driven Architecture**: System components communicate via events and asynchronous messaging. Services SHOULD publish events when state changes occur and subscribe to events to react appropriately.
8. **Dapr-Ready Design**: Architecture MUST be compatible with distributed application runtime patterns. Components SHOULD be designed to work with sidecar architectures and distributed primitives.
9. **Professional UX**: User interfaces MUST provide intuitive navigation, responsive design, and polished user experience suitable for production applications.

**Rationale**: Quality principles ensure code maintains viability across phase evolution. Clean architecture supports incremental complexity without refactoring. MCP statelessness ensures reliable agent operations. Event-driven patterns enable scalability and loose coupling. Dapr-ready design prepares the system for distributed deployment. Professional UX ensures market readiness.

## Technology Constraints

### Core Technology Stack

#### Backend
- **Python**: All backend code MUST use Python
- **FastAPI**: Web framework for API layers (Phase II+)
- **SQLModel**: ORM and data modeling (Phase II+)
- **Neon DB**: Managed PostgreSQL database (Phase II+)

#### Frontend
- **Next.js**: Frontend framework for web interfaces (Phase II+)
- **TypeScript**: Type-safe JavaScript for frontend code (Phase II+)

#### Authentication
- **Better Auth**: Authentication framework for signup/signin (Phase II+)

#### Agent & Integration (Phase III+)
- **OpenAI Agents SDK**: Agent orchestration and tool usage (Phase III+)
- **MCP (Model Context Protocol)**: Agent communication and tool integration (Phase III+)
- **Stateless MCP Tools**: MCP tools MUST NOT store in-memory state and MUST rely on database persistence

#### Infrastructure (Later Phases)
- **Docker**: Containerization (Phase III+)
- **Kubernetes**: Container orchestration (Phase IV+)
- **Kafka**: Event streaming and message queues (Phase IV+)
- **Dapr**: Distributed application runtime (Phase V)
- **Event Streaming**: Event-driven architecture patterns (Phase IV+)
- **Message Queues**: Asynchronous messaging systems (Phase IV+)
- **Event Stores**: Event sourcing and CQRS patterns (Phase IV+)

### Prohibited Technologies
- **Unauthorized Persistence**: Any database or storage not in approved stack (e.g., MongoDB, Redis, filesystem persistence beyond Phase I)
- **Unauthorized Web Frameworks**: Any web framework besides FastAPI (e.g., Flask, Django, Express.js)
- **Unauthorized Frontend**: Any frontend framework besides Next.js (e.g., React, Vue, Angular, Svelte standalone)
- **Unauthorized Auth**: Any authentication framework besides Better Auth (e.g., NextAuth, Auth.js, Clerk) unless formally approved
- **Stateful Services**: Services that maintain implicit state (state MUST be explicit and managed)
- **Alternative Orchestration**: Kubernetes alternatives (e.g., Docker Swarm, Nomad) unless formally approved
- **Alternative Messaging**: Kafka alternatives (e.g., RabbitMQ, AWS SQS) unless formally approved
- **Direct Database Access**: AI agents MUST NOT access database directly; all access MUST be via MCP tools
- **In-Memory State in MCP Tools**: MCP tools MUST NOT store state in memory; all state MUST be persisted in database
- **Synchronous Monolithic Communication**: Direct synchronous calls between services without event-driven patterns (use event-driven architecture instead)
- **Hardcoded Business Logic**: Complex business logic MUST be implemented with configurable event flows, not hardcoded sequences

### Permitted Libraries
- **Python Standard Library**: Preferred for all simple tasks
- **Approved Third-Party Libraries**: Only those in the core technology stack above
- **Justified Additions**: Third-party libraries outside the stack MUST be explicitly justified in spec and approved

### Architectural Patterns
- **PERMITTED**:
  - Clean architecture (domain-driven, hexagonal, or layered)
  - Repository pattern (for database interactions)
  - Service layer pattern
  - CQRS (Command Query Responsibility Segregation) for read/write separation
  - Event Sourcing for maintaining system state as sequence of events
  - Event-Driven Architecture with asynchronous messaging
  - Saga Pattern for distributed transaction management
  - Circuit Breaker pattern for resilient service communication
  - Agent-driven task management
  - Database-backed state management
  - Dapr Building Blocks patterns (service invocation, state management, pub/sub, etc.)
  - Sidecar patterns for infrastructure concerns
  - API Gateway patterns for request routing and transformation
  - Microservice architecture (Phase IV+)
- **PROHIBITED**:
  - Over-engineering patterns not justified by phase requirements
  - Design patterns that add unnecessary abstraction
  - Framework-specific lock-in patterns
  - In-memory state management in MCP tools
  - Direct database access by AI agents
  - Tight coupling between services without event mediation
  - Synchronous blocking communication between services

## Phase Technology Matrix

| Technology | Phase I | Phase II | Phase III | Phase IV | Phase V |
|------------|---------|----------|-----------|----------|---------|
| Python | ✅ | ✅ | ✅ | ✅ | ✅ |
| CLI Interface | ✅ | ✅ | ✅ | ✅ | ✅ |
| In-Memory Storage | ✅ | ❌ | ❌ | ❌ | ❌ |
| FastAPI | ❌ | ✅ | ✅ | ✅ | ✅ |
| SQLModel | ❌ | ✅ | ✅ | ✅ | ✅ |
| Neon DB (PostgreSQL) | ❌ | ✅ | ✅ | ✅ | ✅ |
| Next.js | ❌ | ✅ | ✅ | ✅ | ✅ |
| TypeScript | ❌ | ✅ | ✅ | ✅ | ✅ |
| Better Auth | ❌ | ✅ | ✅ | ✅ | ✅ |
| Docker | ❌ | ❌ | ✅ | ✅ | ✅ |
| OpenAI Agents SDK | ❌ | ❌ | ✅ | ✅ | ✅ |
| MCP | ❌ | ❌ | ✅ | ✅ | ✅ |
| Kubernetes | ❌ | ❌ | ❌ | ✅ | ✅ |
| Kafka | ❌ | ❌ | ❌ | ✅ | ✅ |
| Dapr | ❌ | ❌ | ❌ | ✅ | ✅ |
| Event Streaming | ❌ | ❌ | ❌ | ✅ | ✅ |
| Message Queues | ❌ | ❌ | ❌ | ✅ | ✅ |
| Event Sourcing | ❌ | ❌ | ❌ | ✅ | ✅ |
| CQRS | ❌ | ❌ | ❌ | ✅ | ✅ |
| Professional UI/UX | ❌ | ✅ | ✅ | ✅ | ✅ |

**Notes**:
- ✅ = Technology is in scope for this phase
- ❌ = Technology is out-of-scope for this phase
- Earlier phase technologies remain available in later phases (e.g., CLI remains in Phase V)
- Authentication (Better Auth) is allowed starting Phase II
- Web frontend (Next.js) is allowed starting Phase II
- Neon PostgreSQL is allowed starting Phase II
- AI and agent frameworks (OpenAI Agents SDK, MCP) are NOT allowed until Phase III
- MCP tools must be stateless and rely on database persistence
- AI agents may ONLY interact with the system via MCP tools

## Phase Definitions

### Phase I: In-Memory Console Application
- Python CLI application only
- No persistence (in-memory storage only)
- No network access
- No authentication
- No web interface

### Phase II: Full-Stack Web Application
- Python REST API (FastAPI)
- Neon Serverless PostgreSQL database
- SQLModel for ORM/data modeling
- Next.js frontend (React, TypeScript)
- Better Auth for authentication (signup/signin)
- Full web application architecture

### Phase III: Agent-Enabled Containerized Platform
- Docker containerization
- OpenAI Agents SDK for agent capabilities
- MCP (Model Context Protocol) for agent communication and tool integration
- Stateless MCP tools that rely on database persistence for all state management
- AI agents MAY ONLY interact with the system via MCP tools
- Cloud deployment preparation
- All Phase II technologies continue

### Phase IV: Advanced Cloud Platform
- Kubernetes orchestration
- Advanced cloud infrastructure
- All previous phase technologies continue

### Phase V: Distributed Systems
- Dapr for distributed application runtime with sidecar architecture
- Event streaming and message queuing for asynchronous communication
- Full microservices architecture with event-driven patterns
- Advanced CQRS and event sourcing implementations
- Distributed tracing and observability
- Resilient communication with circuit breakers and retry patterns
- All previous phase technologies continue

## Development Workflow

### Spec-Driven Flow (Mandatory)
1. **Constitution Check**: Verify requirements align with constitution before proceeding
2. **Spec Stage**: Define user stories, requirements, success criteria in `specs/<feature>/spec.md`
3. **Plan Stage**: Create architecture and design in `specs/<feature>/plan.md`
4. **Tasks Stage**: Generate implementation tasks in `specs/<feature>/tasks.md`
5. **Implement Stage**: Execute tasks via AI agents following approved tasks exactly

### Human Role
- Define requirements and approve specifications
- Review and approve plans, tasks, and implementations
- Request clarification or refinement at spec level
- Humans DO NOT write code directly—code written by humans MUST be rejected

### AI Agent Role (Phase III+)
- AI agents MAY ONLY interact with the system via MCP tools (Model Context Protocol)
- MCP tools MUST NOT store in-memory state; all state MUST be persisted in database
- AI agents follow approved tasks exactly and MUST NOT deviate from specifications
- AI agents use OpenAI Agents SDK for orchestration and tool usage

### Quality Gates
- All specs MUST have testable acceptance criteria
- All plans MUST pass Constitution Check (spec-driven, agent behavior, phase governance, quality, technology)
- All implementations MUST match task specifications exactly
- Code violating principles MUST be rejected, even if it "works"
- Technology outside approved phase scope MUST be rejected
- MCP tools MUST be stateless and rely on database persistence
- Event-driven components MUST follow asynchronous messaging patterns
- Dapr-ready implementations MUST be designed for sidecar architecture compatibility
- UX implementations MUST meet professional design standards

### Testing Discipline
- Tests are OPTIONAL unless explicitly requested in spec
- If tests are requested: Red-Green-Refactor MUST be followed strictly
- Test files MUST be in `tests/` directory at repository root
- Backend tests: `pytest` (standard Python testing tool)
- Frontend tests (Phase II+): Jest or Testing Library (to be defined in phase spec)

### Phase Transition
- Phase transition occurs ONLY after all planned features for current phase are complete
- Transition requires new spec and plan for next phase
- No code for next phase may be written before phase transition spec approval
- Technology stack additions for next phase must be explicitly justified

## Governance

### Amendment Procedure
- Constitution changes require explicit consensus via formal amendment spec
- Version follows semantic versioning (MAJOR.MINOR.PATCH)
  - MAJOR: Backward-incompatible changes to core principles, technology stack, or phase structure
  - MINOR: New sections, material expansion of guidance, non-breaking additions
  - PATCH: Wording fixes, clarifications, typo corrections
- All amendment proposals MUST be documented with rationale and impact analysis
- Changes affecting Core Principles (I-IV) require MAJOR version bump
- Changes to Technology Constraints require MAJOR version bump
- Changes to Phase Technology Matrix require MAJOR version bump

### Compliance Review
- All plan artifacts MUST include Constitution Check section
- Constitution violations in plans MUST be justified in Complexity Tracking
- Any unjustified violation results in rejection during review
- All PRs/reviews MUST verify alignment with principles and phase technology matrix
- Technology outside approved phase scope is a critical violation
- MCP tools MUST be validated for statelessness during compliance review
- AI agent interactions MUST be verified to occur only through MCP tools

### Supremacy
This constitution is the supreme governing document for the "Evolution of Todo" project. It supersedes all other practices, guidelines, or conventions. All agents, humans, and processes MUST comply with this constitution without exception.

### Scope Boundaries
This constitution governs Phase I through Phase V of the "Evolution of Todo" project. Each phase is scoped independently by its specification, but all phases remain bound by these core principles and governance rules. Phases beyond V require formal constitution amendment.

**Version**: 2.3.0 | **Ratified**: 2024-12-24 | **Last Amended**: 2026-02-05
