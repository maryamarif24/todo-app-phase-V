/**
 * TypeScript type definitions for event-related functionality.
 */

export interface EventData {
  eventId: string;
  eventType: string;
  taskId: string;
  userId: string;
  payload: Record<string, unknown>;
  timestamp: Date;
}

export interface TaskCreatedEvent extends EventData {
  eventType: 'TASK_CREATED';
  payload: {
    title: string;
    priority: 'LOW' | 'MEDIUM' | 'HIGH';
    dueDate?: Date;
    tags: string[];
    reminderEnabled: boolean;
  };
}

export interface TaskUpdatedEvent extends EventData {
  eventType: 'TASK_UPDATED';
  payload: {
    updatedFields: Partial<{
      title: string;
      description?: string;
      priority: 'LOW' | 'MEDIUM' | 'HIGH';
      dueDate?: Date;
      completed: boolean;
      tags: string[];
      reminderEnabled: boolean;
    }>;
  };
}

export interface TaskCompletedEvent extends EventData {
  eventType: 'TASK_COMPLETED';
  payload: {
    completedAt: Date;
  };
}

export interface ReminderTriggeredEvent extends EventData {
  eventType: 'REMINDER_TRIGGERED';
  payload: {
    reminderTime: Date;
    deliveryMethod: 'email' | 'push_notification' | 'webhook';
  };
}

export interface RecurringTaskGeneratedEvent extends EventData {
  eventType: 'RECURRING_TASK_GENERATED';
  payload: {
    generatedForDate: Date;
    recurrencePattern: 'DAILY' | 'WEEKLY' | 'MONTHLY';
  };
}

export type TaskEvent =
  | TaskCreatedEvent
  | TaskUpdatedEvent
  | TaskCompletedEvent
  | ReminderTriggeredEvent
  | RecurringTaskGeneratedEvent;