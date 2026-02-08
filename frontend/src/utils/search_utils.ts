/**
 * Search/filter utility functions for the Todo application.
 */

import { Task, FilterOptions } from '../types/task';

/**
 * Search tasks by title, description, or tags.
 * @param tasks - Array of tasks to search through
 * @param query - Search query string
 * @returns Filtered array of tasks matching the query
 */
export const searchTasks = (tasks: Task[], query: string): Task[] => {
  if (!query || query.trim() === '') {
    return tasks;
  }

  const lowerQuery = query.toLowerCase();
  return tasks.filter(task => {
    // Check title
    if (task.title.toLowerCase().includes(lowerQuery)) {
      return true;
    }

    // Check description
    if (task.description && task.description.toLowerCase().includes(lowerQuery)) {
      return true;
    }

    // Check tags
    if (task.tags.some(tag => tag.toLowerCase().includes(lowerQuery))) {
      return true;
    }

    return false;
  });
};

/**
 * Filter tasks based on provided filter options.
 * @param tasks - Array of tasks to filter
 * @param filters - Filter options to apply
 * @returns Filtered array of tasks
 */
export const filterTasks = (tasks: Task[], filters: FilterOptions = {}): Task[] => {
  return tasks.filter(task => {
    // Filter by status (completed/pending)
    if (filters.status) {
      if (filters.status === 'completed' && !task.completed) {
        return false;
      }
      if (filters.status === 'pending' && task.completed) {
        return false;
      }
    }

    // Filter by priority
    if (filters.priority) {
      if (task.priority !== filters.priority) {
        return false;
      }
    }

    // Filter by tag
    if (filters.tag) {
      if (!task.tags.includes(filters.tag)) {
        return false;
      }
    }

    // Filter by due date start
    if (filters.dueDateStart) {
      if (!task.dueDate || task.dueDate < filters.dueDateStart) {
        return false;
      }
    }

    // Filter by due date end
    if (filters.dueDateEnd) {
      if (!task.dueDate || task.dueDate > filters.dueDateEnd) {
        return false;
      }
    }

    return true;
  });
};

/**
 * Sort tasks based on the specified criteria.
 * @param tasks - Array of tasks to sort
 * @param sortBy - Field to sort by ('created_at', 'due_date', 'priority')
 * @param order - Sort order ('asc', 'desc')
 * @returns Sorted array of tasks
 */
export const sortTasks = (tasks: Task[], sortBy: 'created_at' | 'due_date' | 'priority' = 'created_at', order: 'asc' | 'desc' = 'asc'): Task[] => {
  const sortedTasks = [...tasks];

  switch (sortBy) {
    case 'created_at':
      sortedTasks.sort((a, b) => {
        const dateA = new Date(a.createdAt);
        const dateB = new Date(b.createdAt);
        return order === 'asc' ? dateA.getTime() - dateB.getTime() : dateB.getTime() - dateA.getTime();
      });
      break;

    case 'due_date':
      sortedTasks.sort((a, b) => {
        // Handle tasks without due dates - they should appear last
        if (!a.dueDate && !b.dueDate) return 0;
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;

        const dateA = new Date(a.dueDate);
        const dateB = new Date(b.dueDate);
        return order === 'asc' ? dateA.getTime() - dateB.getTime() : dateB.getTime() - dateA.getTime();
      });
      break;

    case 'priority':
      const priorityOrder: { [key: string]: number } = { 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3 };
      sortedTasks.sort((a, b) => {
        const priorityA = priorityOrder[a.priority];
        const priorityB = priorityOrder[b.priority];
        return order === 'asc' ? priorityA - priorityB : priorityB - priorityA;
      });
      break;
  }

  return sortedTasks;
};

/**
 * Combine search, filter, and sort operations.
 * @param tasks - Array of tasks to process
 * @param query - Search query string
 * @param filters - Filter options to apply
 * @param sortBy - Field to sort by
 * @param order - Sort order
 * @returns Processed array of tasks
 */
export const processTasks = (
  tasks: Task[],
  query?: string,
  filters?: FilterOptions,
  sortBy?: 'created_at' | 'due_date' | 'priority',
  order?: 'asc' | 'desc'
): Task[] => {
  let result = [...tasks];

  // Apply search if query is provided
  if (query) {
    result = searchTasks(result, query);
  }

  // Apply filters
  if (filters) {
    result = filterTasks(result, filters);
  }

  // Apply sorting
  if (sortBy) {
    result = sortTasks(result, sortBy, order);
  }

  return result;
};