/**
 * Date/time utility functions for the Todo application.
 */

/**
 * Format a date object to a localized string.
 * @param date - The date to format
 * @param options - Optional formatting options
 * @returns Formatted date string
 */
export const formatDate = (date: Date, options?: Intl.DateTimeFormatOptions): string => {
  if (!date) return '';

  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };

  return new Intl.DateTimeFormat('en-US', options || defaultOptions).format(date);
};

/**
 * Check if a date is in the past compared to now.
 * @param date - The date to check
 * @returns True if the date is in the past, false otherwise
 */
export const isPastDue = (date?: Date): boolean => {
  if (!date) return false;
  return date < new Date();
};

/**
 * Calculate the number of days between today and the given date.
 * @param date - The date to compare
 * @returns Number of days between dates (positive if in future, negative if past)
 */
export const calculateDaysUntilDue = (date?: Date): number => {
  if (!date) return 0;

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const dueDate = new Date(date);
  dueDate.setHours(0, 0, 0, 0);

  // Calculate difference in milliseconds and convert to days
  const diffTime = dueDate.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  return diffDays;
};

/**
 * Format a date to ISO string (for API requests).
 * @param date - The date to format
 * @returns ISO string representation of the date
 */
export const formatToISOString = (date: Date): string => {
  if (!date) return '';
  return date.toISOString();
};

/**
 * Parse an ISO string date.
 * @param isoString - The ISO string to parse
 * @returns Date object or null if invalid
 */
export const parseISOString = (isoString: string): Date | null => {
  if (!isoString) return null;

  try {
    const date = new Date(isoString);
    return isNaN(date.getTime()) ? null : date;
  } catch (e) {
    return null;
  }
};

/**
 * Format a date as "X days ago", "today", "tomorrow", etc.
 * @param date - The date to format
 * @returns Relative date string
 */
export const formatRelativeDate = (date: Date): string => {
  if (!date) return '';

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const inputDate = new Date(date);
  inputDate.setHours(0, 0, 0, 0);

  const diffDays = calculateDaysUntilDue(inputDate);

  if (diffDays === 0) {
    return 'Today';
  } else if (diffDays === 1) {
    return 'Tomorrow';
  } else if (diffDays === -1) {
    return 'Yesterday';
  } else if (diffDays > 0) {
    return `In ${diffDays} day${diffDays !== 1 ? 's' : ''}`;
  } else {
    return `${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? 's' : ''} ago`;
  }
};