/**
 * API client for the Todo application with advanced features.
 *
 * This module provides a client for interacting with the backend API endpoints.
 */

import { Task, TaskFormData, FilterOptions, TaskQuery } from '../types/task';

// Base API URL - configurable based on environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

interface ApiErrorResponse {
  error: string;
  message: string;
  details?: Record<string, unknown>;
}

// Generic API call function
const apiCall = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;

  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const errorResponse: ApiErrorResponse = await response.json().catch(() => ({
        error: 'Unknown Error',
        message: `HTTP Error ${response.status}`,
      }));

      throw new Error(errorResponse.message || `HTTP Error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API call failed: ${url}`, error);
    throw error;
  }
};

// Task API functions
export const taskApi = {
  /**
   * Get all tasks with optional filtering, sorting, and pagination.
   */
  getTasks: async (filters?: FilterOptions, limit: number = 20, offset: number = 0): Promise<{ tasks: Task[]; total: number; offset: number; limit: number }> => {
    const params = new URLSearchParams({
      ...(filters?.status && { status: filters.status }),
      ...(filters?.priority && { priority: filters.priority }),
      ...(filters?.tag && { tag: filters.tag }),
      ...(filters?.dueDateStart && { due_date_start: filters.dueDateStart.toISOString() }),
      ...(filters?.dueDateEnd && { due_date_end: filters.dueDateEnd.toISOString() }),
      ...(filters?.sortBy && { sort_by: filters.sortBy }),
      ...(filters?.order && { order: filters.order }),
      limit: limit.toString(),
      offset: offset.toString(),
    });

    return apiCall(`${API_BASE_URL}/tasks?${params.toString()}`);
  },

  /**
   * Create a new task with advanced features.
   */
  createTask: async (taskData: TaskFormData): Promise<Task> => {
    return apiCall<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  /**
   * Get a specific task by ID.
   */
  getTaskById: async (taskId: string): Promise<Task> => {
    return apiCall<Task>(`/tasks/${taskId}`);
  },

  /**
   * Update an existing task.
   */
  updateTask: async (taskId: string, taskData: Partial<TaskFormData>): Promise<Task> => {
    return apiCall<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  /**
   * Delete a task by ID.
   */
  deleteTask: async (taskId: string): Promise<void> => {
    await apiCall(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },

  /**
   * Search tasks with query and filters.
   */
  searchTasks: async (query: string, filters?: FilterOptions, limit: number = 20): Promise<{ results: Task[]; total: number; query: string; took_ms: number }> => {
    const searchQuery: TaskQuery = {
      query,
      filters,
      limit,
      offset: 0, // For search, we may not use offset in the same way
    };

    return apiCall('/tasks/search', {
      method: 'POST',
      body: JSON.stringify(searchQuery),
    });
  },

  /**
   * Toggle task completion status.
   */
  toggleTaskCompletion: async (taskId: string): Promise<Task> => {
    return apiCall<Task>(`/tasks/${taskId}/toggle-complete`, {
      method: 'POST',
    });
  },
};

// Recurring Task API functions
export const recurringTaskApi = {
  /**
   * Create a new recurring task pattern.
   */
  createRecurringPattern: async (patternData: { taskId: string; frequency: string; endDate?: string }): Promise<{ id: string; taskId: string; frequency: string; endDate?: string; createdAt: string }> => {
    return apiCall('/tasks/recurring', {
      method: 'POST',
      body: JSON.stringify(patternData),
    });
  },

  /**
   * Get a recurring task pattern by ID.
   */
  getRecurringPattern: async (patternId: string): Promise<{ id: string; taskId: string; frequency: string; endDate?: string; createdAt: string }> => {
    return apiCall(`/tasks/recurring/${patternId}`);
  },

  /**
   * Update a recurring task pattern.
   */
  updateRecurringPattern: async (patternId: string, patternData: { frequency?: string; endDate?: string }): Promise<{ id: string; taskId: string; frequency: string; endDate?: string; createdAt: string }> => {
    return apiCall(`/tasks/recurring/${patternId}`, {
      method: 'PUT',
      body: JSON.stringify(patternData),
    });
  },

  /**
   * Delete a recurring task pattern.
   */
  deleteRecurringPattern: async (patternId: string): Promise<void> => {
    await apiCall(`/tasks/recurring/${patternId}`, {
      method: 'DELETE',
    });
  },
};

// Tag API functions
export const tagApi = {
  /**
   * Get all tags for the current user.
   */
  getUserTags: async (): Promise<Array<{ id: string; name: string; color: string; userId: string; createdAt: string; updatedAt: string }>> => {
    return apiCall('/tags');
  },

  /**
   * Create a new tag.
   */
  createTag: async (tagData: { name: string; color?: string }): Promise<{ id: string; name: string; color: string; userId: string; createdAt: string; updatedAt: string }> => {
    return apiCall('/tags', {
      method: 'POST',
      body: JSON.stringify(tagData),
    });
  },
};

// General API utilities
export const apiUtils = {
  /**
   * Check if the API is reachable.
   */
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  },
};

const apiClient = {
  taskApi,
  recurringTaskApi,
  tagApi,
  apiUtils,
};

export default apiClient;