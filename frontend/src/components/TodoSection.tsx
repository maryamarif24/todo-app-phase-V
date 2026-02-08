'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import type { Todo, TodoListResponse, CreateTodoResponse } from '@/types';
import { useAuth } from './auth/auth-provider';

interface TodoSectionProps {
  isAuthenticated: boolean;
}

export default function TodoSection({ isAuthenticated }: TodoSectionProps) {
  const { session } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [newTodoPriority, setNewTodoPriority] = useState<'LOW' | 'MEDIUM' | 'HIGH'>('MEDIUM');
  const [isAdding, setIsAdding] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (isAuthenticated) {
      fetchTodos();
    }
  }, [isAuthenticated]);

  const fetchTodos = async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    const response = await api.get<TodoListResponse>('/todos');

    if (response.error) {
      setError(response.error);
    } else if (response.data) {
      setTodos(response.data.todos);
    }

    setLoading(false);
  };

  const handleToggle = async (todoId: string) => {
    const response = await api.patch<Todo>(`/todos/${todoId}/toggle`);

    if (response.data) {
      setTodos(todos.map(t => t.id === todoId ? response.data! : t));
    }
  };

  const handleDelete = async (todoId: string) => {
    if (!confirm('Are you sure you want to delete this todo?')) return;

    const response = await api.delete<{ message: string }>(`/todos/${todoId}`);

    if (!response.error) {
      setTodos(todos.filter(t => t.id !== todoId));
    }
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    // Check if user is authenticated before attempting to add todo
    if (!session?.token) {
      setError('You must be logged in to add a todo. Please sign in.');
      return;
    }

    setIsAdding(true);
    const request = {
      title: newTodoTitle.trim(),
      description: newTodoDescription.trim() || undefined,
      priority: newTodoPriority,
    };

    const response = await api.post<CreateTodoResponse>('/todos', request);

    if (response.error) {
      setError(response.error);
      setIsAdding(false);
      console.error('Failed to add todo:', response.error); // Debug log
      // Additional debugging information
      console.error('Request payload:', request);
      return;
    }

    setNewTodoTitle('');
    setNewTodoDescription('');
    setNewTodoPriority('MEDIUM');
    setIsAdding(false);
    fetchTodos();
  };

  const pendingTodos = todos.filter(todo => !todo.is_complete);
  const completedTodos = todos.filter(todo => todo.is_complete);

  // Calculate progress percentage
  const totalTodos = todos.length;
  const progressPercentage = totalTodos > 0
    ? Math.round((completedTodos.length / totalTodos) * 100)
    : 0;

  if (!isAuthenticated) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 mt-8">
        <h2 className="text-xl font-bold mb-4 text-center" style={{ color: "#7F1734" }}>Welcome to Worksy Todo</h2>
        <p className="text-gray-600 text-center mb-6">
          Sign in to start managing your tasks and todos efficiently.
        </p>
        <div className="flex justify-center space-x-4">
          <a 
            href="/signin" 
            className="px-6 py-3 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors"
          >
            Sign In
          </a>
          <a 
            href="/signup" 
            className="px-6 py-3 border border-pink-500 text-pink-600 rounded-lg hover:bg-pink-50 transition-colors"
          >
            Sign Up
          </a>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Loading todos...</p>
      </div>
    );
  }

  return (
    <div className="mt-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold" style={{ color: 'black' }}>Your Todos</h2>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Progress and Add Todo Sections */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Progress Section */}
        <div
          className="rounded-3xl p-6 relative overflow-hidden"
          style={{
            background: 'linear-gradient(135deg, #ff69b4 0%, #ff1493 50%, #000000 100%)'
          }}
        >
          {/* Subtle abstract geometric pattern */}
          <div className="absolute inset-0 opacity-5 pointer-events-none">
            <div className="absolute top-4 right-4 w-32 h-32 rounded-full" style={{ background: 'white' }} />
            <div className="absolute bottom-4 left-4 w-24 h-24 rounded-full" style={{ background: 'white' }} />
            <div className="absolute top-1/2 right-1/4 w-16 h-16 rotate-45" style={{ background: 'white' }} />
          </div>

          <div className="relative z-10">
            <div className="flex justify-between items-center mb-3">
              <span className="text-lg font-semibold text-white">Daily Progress</span>
              <span className="text-2xl font-bold text-white">
                {progressPercentage}%
              </span>
            </div>
            <div className="w-full bg-white bg-opacity-20 rounded-full h-4">
              <div
                className="h-4 rounded-full transition-all duration-500 ease-out shadow-lg"
                style={{
                  width: `${progressPercentage}%`,
                  background: 'linear-gradient(90deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)'
                }}
              />
            </div>
            <div className="flex justify-between mt-3 text-sm text-white text-opacity-90">
              <span>{completedTodos.length} completed</span>
              <span>{pendingTodos.length} pending</span>
            </div>
          </div>
        </div>

        {/* Add Todo Section */}
        <div className="bg-white rounded-3xl shadow-lg p-6 relative overflow-hidden">
          {/* Subtle abstract geometric pattern */}
          <div className="absolute inset-0 opacity-5 pointer-events-none">
            <div className="absolute top-4 left-4 w-20 h-20 rounded-full" style={{ background: 'rgb(255, 182, 193)' }} />
            <div className="absolute bottom-4 right-4 w-16 h-16 rounded-full" style={{ background: 'rgb(255, 107, 157)' }} />
            <div className="absolute top-1/2 left-1/4 w-12 h-12 rotate-45" style={{ background: 'rgb(196, 69, 105)' }} />
          </div>

          <div className="relative z-10">
            <h3 className="text-lg font-semibold mb-4" style={{ color: 'black' }}>Add New Todo</h3>
            <form onSubmit={handleAddTodo} className="flex flex-col gap-4">
              <input
                type="text"
                value={newTodoTitle}
                onChange={(e) => setNewTodoTitle(e.target.value)}
                placeholder="What needs to be done?"
                className="w-full px-3 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 text-black"
                style={{ borderColor: '#d1d5db', color: 'black', '--tw-ring-color': '#ff69b4' } as React.CSSProperties}
                maxLength={200}
              />
              <textarea
                value={newTodoDescription}
                onChange={(e) => setNewTodoDescription(e.target.value)}
                placeholder="Add more details... (optional)"
                className="w-full px-3 py-2 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 h-20 text-black"
                style={{ borderColor: '#d1d5db', color: 'black', '--tw-ring-color': '#ff69b4' } as React.CSSProperties}
                maxLength={2000}
              />
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <label className="text-sm font-medium text-black">Priority:</label>
                  <select
                    value={newTodoPriority}
                    onChange={(e) => setNewTodoPriority(e.target.value as 'LOW' | 'MEDIUM' | 'HIGH')}
                    className="px-3 py-1 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 text-black"
                    style={{ borderColor: '#d1d5db', color: 'black', '--tw-ring-color': '#ff69b4' } as React.CSSProperties}
                  >
                    <option value="LOW">Low</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HIGH">High</option>
                  </select>
                </div>
                <button
                  type="submit"
                  disabled={isAdding || !newTodoTitle.trim()}
                  className="px-6 py-2 text-white rounded-full hover:opacity-90 disabled:opacity-50 transition"
                  style={{ backgroundColor: 'black' }}
                >
                  {isAdding ? 'Adding...' : 'Add Todo'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Pending and Completed Sections */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Pending Section */}
        <div className="bg-white rounded-3xl shadow-lg p-6" style={{ backgroundColor: 'white' }}>
          <h3 className="text-lg font-semibold mb-4 pb-2 border-b" style={{ color: 'black', borderColor: '#d1d5db' }}>
            Pending ({pendingTodos.length})
          </h3>

          {pendingTodos.length === 0 ? (
            <p className="text-pink-600 text-center py-8" style={{ color: '#ff69b4' }}>No pending todos</p>
          ) : (
            <div className="space-y-3">
              {pendingTodos.map((todo) => (
                <div
                  key={todo.id}
                  className="bg-gray-50 rounded-2xl shadow p-4 flex items-center gap-4"
                  style={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                >
                  <input
                    type="checkbox"
                    checked={todo.is_complete}
                    onChange={() => handleToggle(todo.id)}
                    className="w-5 h-5"
                    style={{ accentColor: '#ff69b4' }}
                  />
                  <div className="flex-1">
                    <h3 className="font-medium" style={{ color: 'black' }}>{todo.title}</h3>
                    {todo.description && (
                      <p className="text-sm text-gray-700 mt-1" style={{ color: 'black' }}>{todo.description}</p>
                    )}
                    <p className="text-xs text-gray-500 mt-2" style={{ color: 'black' }}>
                      Created: {mounted ? new Date(todo.created_at).toLocaleDateString() : ''}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleDelete(todo.id)}
                      className="px-3 py-1 text-sm rounded-full text-gray-500 hover:text-pink-700 transition-colors"
                      style={{ color: 'black' }}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M3 6h18" />
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Completed Section */}
        <div className="bg-white rounded-3xl shadow-lg p-6" style={{ backgroundColor: 'white' }}>
          <h3 className="text-lg font-semibold mb-4 pb-2 border-b" style={{ color: 'black', borderColor: '#d1d5db' }}>
            Completed ({completedTodos.length})
          </h3>

          {completedTodos.length === 0 ? (
            <p className="text-pink-600 text-center py-8" style={{ color: '#ff69b4' }}>No completed todos yet</p>
          ) : (
            <div className="space-y-3">
              {completedTodos.map((todo) => (
                <div
                  key={todo.id}
                  className="bg-gray-50 rounded-2xl shadow p-4 flex items-center gap-4"
                  style={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                >
                  <input
                    type="checkbox"
                    checked={todo.is_complete}
                    onChange={() => handleToggle(todo.id)}
                    className="w-5 h-5"
                    style={{ accentColor: '#ff69b4' }}
                  />
                  <div className="flex-1">
                    <h3 className="font-medium line-through" style={{ color: 'black', textDecorationColor: 'black' }}>{todo.title}</h3>
                    {todo.description && (
                      <p className="text-sm text-gray-500 mt-1 line-through" style={{ color: 'black', textDecorationColor: 'black' }}>{todo.description}</p>
                    )}
                    <p className="text-xs text-gray-400 mt-2" style={{ color: 'black' }}>
                      Created: {mounted ? new Date(todo.created_at).toLocaleDateString() : ''}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleDelete(todo.id)}
                      className="px-3 py-1 text-sm rounded-full text-gray-500 hover:text-pink-700 transition-colors"
                      style={{ color: 'black' }}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M3 6h18" />
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}