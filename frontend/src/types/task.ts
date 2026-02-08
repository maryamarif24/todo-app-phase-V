/**
 * TypeScript type definitions for task-related functionality.
 */

export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  dueDate?: Date;
  completed: boolean;
  completedAt?: Date;
  tags: string[];
  reminderEnabled: boolean;
  reminderTime?: string;
  createdAt: Date;
  updatedAt: Date;
  recurrencePatternId?: string;
}

export interface Tag {
  id: string;
  name: string;
  userId: string;
  color: string;
  createdAt: Date;
}

export interface RecurringTaskPattern {
  id: string;
  userId: string;
  frequency: 'DAILY' | 'WEEKLY' | 'MONTHLY';
  interval: number;
  endConditionType: 'COUNT' | 'DATE' | 'NEVER';
  endAfterCount?: number;
  endDate?: Date;
  weekdaysMask?: number;
  dayOfMonth?: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority?: 'LOW' | 'MEDIUM' | 'HIGH';
  dueDate?: Date;
  tags: string[];
  reminderEnabled: boolean;
  reminderTime?: string;
}

export interface FilterOptions {
  status?: 'pending' | 'completed';
  priority?: 'LOW' | 'MEDIUM' | 'HIGH';
  tag?: string;
  dueDateStart?: Date;
  dueDateEnd?: Date;
  sortBy?: 'created_at' | 'due_date' | 'priority';
  order?: 'asc' | 'desc';
}

export interface TaskQuery {
  query: string;
  filters?: FilterOptions;
  limit: number;
  offset: number;
}