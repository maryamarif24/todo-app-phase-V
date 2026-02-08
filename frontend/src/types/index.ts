/**
 * TypeScript type definitions for the Todo application.
 *
 * This module provides TypeScript interfaces that mirror the
 * API response structures for type-safe frontend code.
 */

/**
 * User type matching the API response.
 */
export interface User {
  id: string;
  email: string;
  created_at?: string;
}


/**
 * Todo item type matching the API response.
 */
export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_complete: boolean;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  created_at: string;
  updated_at: string;
}


/**
 * Response from GET /todos endpoint.
 */
export interface TodoListResponse {
  todos: Todo[];
}


/**
 * Response from POST /todos endpoint.
 */
export interface CreateTodoResponse {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}


/**
 * Request body for POST /todos endpoint.
 */
export interface CreateTodoRequest {
  title: string;
  description?: string;
}


/**
 * Request body for PUT /todos/:id endpoint.
 */
export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  is_complete?: boolean;
}


/**
 * Request body for POST /auth/signup endpoint.
 */
export interface SignupRequest {
  email: string;
  password: string;
}


/**
 * Response from POST /auth/signup endpoint.
 */
export interface SignupResponse {
  user: User;
  session: {
    token: string;
    expires_at: string;
  };
}


/**
 * Request body for POST /auth/signin endpoint.
 */
export interface SigninRequest {
  email: string;
  password: string;
}


/**
 * Response from POST /auth/signin endpoint.
 */
export interface SigninResponse {
  user: User;
  session: {
    token: string;
    expires_at: string;
  };
}


/**
 * Generic error response.
 */
export interface ErrorResponse {
  detail: string;
}
