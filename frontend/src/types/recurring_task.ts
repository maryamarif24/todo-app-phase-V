/**
 * TypeScript type definitions for recurring task functionality.
 */

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

export interface RecurringTaskFormData {
  frequency: 'DAILY' | 'WEEKLY' | 'MONTHLY';
  interval: number;
  endConditionType: 'COUNT' | 'DATE' | 'NEVER';
  endAfterCount?: number;
  endDate?: Date;
  weekdaysMask?: number;
  dayOfMonth?: number;
}

export interface RecurringTaskGenerationParams {
  patternId: string;
  startDate: Date;
  endDate: Date;
}