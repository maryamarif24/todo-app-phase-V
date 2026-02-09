# Data Model Design: Advanced Features for Phase 5 (Part A)

**Date**: 2026-02-05
**Feature**: Advanced Features for Phase 5 (Part A)
**Branch**: 001-advanced-todo-features

## Overview

This document outlines the extended data model for Phase 5 Advanced Features, building upon the existing task management system with enhanced capabilities for priorities, due dates, tags, recurring tasks, and event-driven architecture.

## 1. Core Entity Extensions

### 1.1 Task Entity (Extended)

**Current Fields (from Phase II)**:
- id: UUID (Primary Key)
- title: VARCHAR(255) - Task title
- description: TEXT - Optional task description
- completed: BOOLEAN - Completion status
- user_id: UUID - Foreign key to user who owns the task
- created_at: TIMESTAMP - Creation timestamp
- updated_at: TIMESTAMP - Last update timestamp

**New Fields**:
- priority: VARCHAR(20) - Task priority level (LOW, MEDIUM, HIGH) - Default: MEDIUM
- due_date: TIMESTAMP - Optional deadline for task completion
- tags: TEXT[] - Array of tag labels for categorization (e.g., ['work', 'personal'])
- completed_at: TIMESTAMP - Timestamp when task was marked as complete (nullable)
- recurrence_pattern_id: UUID - Foreign key to recurring pattern (nullable)
- reminder_enabled: BOOLEAN - Whether reminder notifications are enabled - Default: FALSE
- reminder_time: INTERVAL - Time before due_date to trigger reminder (e.g., '1 day')

**Validation Rules**:
- priority must be one of: 'LOW', 'MEDIUM', 'HIGH'
- due_date must be in the future if provided
- tags array must contain 0-10 tags, each tag 1-50 characters
- if reminder_enabled=true, due_date must be provided

### 1.2 Tag Entity (New)

**Fields**:
- id: UUID (Primary Key)
- name: VARCHAR(50) - Unique tag name
- user_id: UUID - Foreign key to user who created the tag
- color: VARCHAR(7) - Hex color code for tag display (e.g., '#FF5733')
- created_at: TIMESTAMP - Creation timestamp

**Validation Rules**:
- name must be unique per user
- name must be 1-50 characters
- color must follow hex format (#XXXXXX)
- Only 50 unique tags per user

### 1.3 RecurringTaskPattern Entity (New)

**Fields**:
- id: UUID (Primary Key)
- user_id: UUID - Foreign key to user who created the pattern
- frequency: VARCHAR(20) - Recurrence frequency (DAILY, WEEKLY, MONTHLY)
- interval: INTEGER - Interval multiplier (e.g., every 2 weeks: interval=2, frequency=WEEKLY)
- end_condition_type: VARCHAR(20) - End condition type (COUNT, DATE, NEVER)
- end_after_count: INTEGER - Number of occurrences (for COUNT type)
- end_date: TIMESTAMP - End date (for DATE type)
- weekdays_mask: INTEGER - Bitmask for days of week (for WEEKLY - 1=Mon, 2=Tue, etc.)
- day_of_month: INTEGER - Day of month (for MONTHLY - 1-31)
- created_at: TIMESTAMP - Creation timestamp
- updated_at: TIMESTAMP - Last update timestamp

**Validation Rules**:
- frequency must be one of: 'DAILY', 'WEEKLY', 'MONTHLY'
- interval must be 1-365
- if end_condition_type='COUNT', end_after_count must be 1-1000
- if end_condition_type='DATE', end_date must be in the future
- if frequency='WEEKLY', weekdays_mask must have at least one bit set
- if frequency='MONTHLY', day_of_month must be 1-31

### 1.4 Reminder Entity (New)

**Fields**:
- id: UUID (Primary Key)
- task_id: UUID - Foreign key to the associated task
- scheduled_time: TIMESTAMP - When reminder should be triggered
- sent: BOOLEAN - Whether reminder has been sent - Default: FALSE
- sent_at: TIMESTAMP - When reminder was actually sent (nullable)
- delivered: BOOLEAN - Whether reminder was delivered successfully - Default: FALSE
- delivery_attempts: INTEGER - Number of delivery attempts - Default: 0
- created_at: TIMESTAMP - Creation timestamp
- updated_at: TIMESTAMP - Last update timestamp

**Validation Rules**:
- scheduled_time must be in the future
- delivery_attempts must be 0-5

## 2. Relationship Diagram

```
User (1) <---> (Many) Task
Task (1) <---> (0..1) RecurringTaskPattern (via recurrence_pattern_id)
Task (Many) <---> (Many) Tag (via task_tags junction table)
Task (1) <---> (Many) Reminder (via task_id)
Tag (1) <---> (Many) User (via user_id)
```

## 3. Junction Tables

### 3.1 TaskTag (Many-to-Many between Task and Tag)

**Fields**:
- task_id: UUID - Foreign key to Task
- tag_id: UUID - Foreign key to Tag
- assigned_at: TIMESTAMP - When tag was assigned to task

**Primary Key**: (task_id, tag_id)

## 4. Event Models

### 4.1 TaskEvent Entity (New)

**Fields**:
- id: UUID (Primary Key)
- event_type: VARCHAR(50) - Type of event (TASK_CREATED, TASK_UPDATED, TASK_COMPLETED, REMINDER_TRIGGERED)
- task_id: UUID - Foreign key to the associated task
- payload: JSONB - Event-specific data payload
- occurred_at: TIMESTAMP - When event occurred
- processed: BOOLEAN - Whether event has been processed - Default: FALSE
- processed_at: TIMESTAMP - When event was processed (nullable)

**Validation Rules**:
- event_type must be one of: 'TASK_CREATED', 'TASK_UPDATED', 'TASK_COMPLETED', 'REMINDER_TRIGGERED'
- payload must be valid JSON
- processed_at can only be set when processed=true

## 5. Indexing Strategy

### 5.1 Primary Indexes
- Task: PRIMARY KEY (id)
- Task: INDEX (user_id, created_at) - For user-specific task retrieval
- Task: INDEX (user_id, due_date) - For due date queries
- Task: INDEX (user_id, priority) - For priority-based queries
- Task: INDEX (user_id, completed) - For completion status queries
- Task: INDEX (recurrence_pattern_id) - For recurring task lookup

### 5.2 Composite Indexes
- Task: INDEX (user_id, completed, priority, due_date) - For common filter combinations
- Task: GIN (tags) - For tag-based filtering
- Reminder: INDEX (scheduled_time, sent) - For active reminder queries
- Reminder: INDEX (task_id, scheduled_time) - For task-specific reminder queries

### 5.3 Specialized Indexes
- Task: INDEX ON due_date WHERE due_date IS NOT NULL AND completed = false - For upcoming due dates
- Task: INDEX ON created_at WHERE created_at >= NOW() - 30 days - For recent activity
- TaskEvent: INDEX (occurred_at, processed) - For event processing
- TaskEvent: INDEX (task_id, event_type) - For task-specific event queries

## 6. Audit Trail Considerations

### 6.1 Task History
- Maintain record of task modifications in TaskEvent table
- Track who changed what and when for audit purposes
- Store before/after states for debugging and compliance

## 7. Data Integrity Constraints

### 7.1 Foreign Key Constraints
- Task.user_id references User.id (CASCADE DELETE)
- Task.recurrence_pattern_id references RecurringTaskPattern.id (SET NULL on delete)
- Reminder.task_id references Task.id (CASCADE DELETE)
- TaskTag.task_id references Task.id (CASCADE DELETE)
- TaskTag.tag_id references Tag.id (CASCADE DELETE)
- Tag.user_id references User.id (CASCADE DELETE)
- RecurringTaskPattern.user_id references User.id (CASCADE DELETE)

### 7.2 Check Constraints
- Task.priority IN ('LOW', 'MEDIUM', 'HIGH')
- Task.due_date > CURRENT_TIMESTAMP (when provided)
- RecurringTaskPattern.interval BETWEEN 1 AND 365
- RecurringTaskPattern.end_after_count BETWEEN 1 AND 1000
- RecurringTaskPattern.day_of_month BETWEEN 1 AND 31

## 8. Performance Considerations

### 8.1 Partitioning Strategy
- Consider time-based partitioning for TaskEvent table if event volume grows
- Monthly partitions for events older than 6 months to improve query performance

### 8.2 Materialized Views
- Materialized view for complex dashboard queries (monthly/quarterly summaries)
- Cache frequently joined data for reporting purposes

## 9. Migration Path

### 9.1 Forward Migration
- Add nullable columns to existing Task table
- Create new tables (Tag, RecurringTaskPattern, Reminder, TaskEvent, TaskTag)
- Add indexes to optimize new queries
- Populate initial data from existing records where applicable

### 9.2 Backward Compatibility
- New columns default to non-breaking values
- Existing functionality remains unchanged
- New features only activate when explicitly used
- API responses maintain backward compatibility for existing fields

## 10. Security Considerations

### 10.1 Data Access Control
- All entities must include user_id for multi-tenancy
- Foreign key constraints enforce data ownership
- Queries must always filter by user_id to prevent unauthorized access

### 10.2 Sensitive Data
- No sensitive data stored in the new entities
- Reminder times are non-sensitive scheduling information
- Tags are user-generated content without PII