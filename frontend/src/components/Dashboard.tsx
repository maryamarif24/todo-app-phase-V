'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from './auth/auth-provider';
import { api } from '@/lib/api';
import {
  Inbox,
  Calendar,
  Clock,
  Plus,
  CheckCircle2,
  Circle,
  Flag,
  MoreVertical,
  LogOut,
  ChevronDown,
  Search,
  X
} from 'lucide-react';

interface TodoResponse {
  id: string;
  title: string;
  is_complete: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  created_at: string;
}

interface Task {
  id: string;
  title: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
  createdAt: string;
}

const Dashboard = () => {
  const router = useRouter();
  const { user, signout, updateUser } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Function to refresh tasks after chatbot operations
  const refreshTasks = useCallback(async () => {
    await fetchTasks();
  }, []);

  useEffect(() => {
    fetchTasks();
  }, []);

  // Listen for custom events from the chat widget to refresh tasks
  useEffect(() => {
    const handleRefreshTasks = () => {
      refreshTasks();
    };

    window.addEventListener('refreshTasks', handleRefreshTasks);
    return () => {
      window.removeEventListener('refreshTasks', handleRefreshTasks);
    };
  }, [refreshTasks]);

  const fetchTasks = async () => {
    try {
      // Fetch tasks from the API using the api service
      const response = await api.get<{todos: TodoResponse[]} | null>('/todos');

      if (response.error) {
        throw new Error(response.error);
      }

      // Map the response to the Task type
      if (response.data && Array.isArray(response.data.todos)) {
        const mappedTasks = response.data.todos.map((todo) => ({
          id: todo.id,
          title: todo.title,
          completed: todo.is_complete,
          priority: todo.priority || 'medium',
          dueDate: todo.due_date || undefined,
          createdAt: todo.created_at
        }));

        setTasks(mappedTasks);
      } else {
        setTasks([]);
      }
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);

      // Fallback to mock data if API fails
      const mockTasks: Task[] = [
        {
          id: '1',
          title: 'Design new landing page',
          completed: false,
          priority: 'high',
          dueDate: '2024-02-10',
          createdAt: '2024-02-05'
        },
        {
          id: '2',
          title: 'Review quarterly reports',
          completed: false,
          priority: 'medium',
          dueDate: '2024-02-08',
          createdAt: '2024-02-04'
        },
        {
          id: '3',
          title: 'Schedule team meeting',
          completed: true,
          priority: 'low',
          createdAt: '2024-02-03'
        },
        {
          id: '4',
          title: 'Update documentation',
          completed: false,
          priority: 'medium',
          dueDate: '2024-02-12',
          createdAt: '2024-02-05'
        }
      ];
      setTasks(mockTasks);
    }
  };

  const [newTask, setNewTask] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [searchQuery, setSearchQuery] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [mobileRightSidebarOpen, setMobileRightSidebarOpen] = useState(false);
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
  const [showEditProfileModal, setShowEditProfileModal] = useState(false);
  const [editingName, setEditingName] = useState(user?.email.split('@')[0] || '');
  const [editingEmail, setEditingEmail] = useState(user?.email || '');
  const [activeFilter, setActiveFilter] = useState<'all' | 'completed' | 'pending'>('all');

  useEffect(() => {
    // Update editingName and editingEmail when user object changes
    setEditingName(user?.email?.split('@')[0] || '');
    setEditingEmail(user?.email || '');
  }, [user]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (userMenuOpen && !target.closest('.user-menu-container')) {
        setUserMenuOpen(false);
      }
      if (mobileSearchOpen && !target.closest('.mobile-search-container')) {
        setMobileSearchOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [userMenuOpen, mobileSearchOpen]);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Close mobile menus when resizing to desktop
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setMobileSidebarOpen(false);
        setMobileRightSidebarOpen(false);
        setMobileSearchOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleAddTask = async () => {
    if (newTask.trim() === '') return;

    try {
      // Call the API to add the task
      const response = await api.post('/todos', { 
        title: newTask,
        priority: newTaskPriority
      });
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      // Refresh the task list to include the new task
      await fetchTasks();
      setNewTask('');
    } catch (err) {
      setError('Failed to add task');
      console.error('Error adding task:', err);
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    try {
      // Call the API to toggle the task completion
      const response = await api.patch(`/todos/${id}/toggle`);
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      // Refresh the task list to reflect the change
      await fetchTasks();
    } catch (err) {
      setError('Failed to update task');
      console.error('Error toggling task:', err);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      // Call the API to delete the task
      const response = await api.delete(`/todos/${id}`);
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      // Refresh the task list to reflect the deletion
      await fetchTasks();
      setOpenDropdown(null);
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const toggleDropdown = (taskId: string) => {
    setOpenDropdown(openDropdown === taskId ? null : taskId);
  };

  const updateTaskPriority = async (id: string, priority: 'low' | 'medium' | 'high') => {
    try {
      console.log('Updating task priority:', { id, priority }); // Debug log
      
      // Call the API to update the task priority
      const response = await api.patch(`/todos/${id}`, {
        priority: priority
      });
      
      console.log('Priority update response:', response); // Debug log
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      // Refresh the task list to reflect the change
      await fetchTasks();
      setOpenDropdown(null);
    } catch (err) {
      setError('Failed to update task priority');
      console.error('Error updating task priority:', err);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-500';
      case 'medium': return 'text-yellow-500';
      case 'low': return 'text-green-500';
      default: return 'text-gray-500';
    }
  };


  const today = new Date();
  const formattedDate = today.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  });

  // Filter tasks based on search query and active filter
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (activeFilter === 'completed') {
      return matchesSearch && task.completed;
    } else if (activeFilter === 'pending') {
      return matchesSearch && !task.completed;
    } else {
      return matchesSearch;
    }
  });

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-pink-50 text-gray-900">
      {/* Mobile menu button */}
      <div className="md:hidden fixed top-4 left-4 z-50">
        <button
          onClick={() => setMobileSidebarOpen(true)}
          className="p-2 rounded-lg bg-black text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Mobile right sidebar button */}
      <div className="md:hidden fixed top-4 right-4 z-50">
        <button
          onClick={() => setMobileRightSidebarOpen(true)}
          className="p-2 rounded-lg bg-pink-500 text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </button>
      </div>

      {/* Sidebar - Mobile Overlay */}
      {mobileSidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 md:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        ></div>
      )}

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-20'} ${mobileSidebarOpen ? 'fixed inset-y-0 z-50' : 'hidden md:flex'} bg-gradient-to-b from-pink-400 to-pink-600 border border-pink-500 rounded-3xl shadow-lg shadow-pink-200/50 flex flex-col transition-all duration-300 m-4 relative overflow-hidden`}>
        {/* Abstract geometric pattern overlay */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-10 right-4 w-16 h-16 rounded-full bg-pink-300/20"></div>
          <div className="absolute top-1/3 right-2 w-8 h-8 rounded-full bg-pink-200/30"></div>
          <div className="absolute bottom-20 right-6 w-12 h-12 rounded-lg bg-pink-300/15 transform rotate-45"></div>
          <div className="absolute bottom-1/3 right-3 w-6 h-6 rounded-full bg-pink-200/25"></div>
        </div>
        
        <div className="p-6 pb-4 border-b border-pink-500/50 flex justify-between items-center relative z-10">
          <h1 className={`font-bold text-xl ${sidebarOpen ? 'block' : 'hidden'} text-white`} style={{ color: 'white' }}>TodoApp</h1>
          <button
            onClick={() => {
              if (window.innerWidth < 768) {
                setMobileSidebarOpen(false);
              } else {
                toggleSidebar();
              }
            }}
            className="p-1 rounded hover:bg-pink-500/50"
          >
            <ChevronDown className={`w-4 h-4 ${sidebarOpen ? 'rotate-180' : ''}`} style={{ color: 'white' }} />
          </button>
        </div>

        <nav className="flex-1 p-4 space-y-2 relative z-10">
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-xl bg-pink-500/30 text-white" style={{ color: 'white' }}>
            <Inbox className="w-5 h-5" style={{ color: 'white' }} />
            {sidebarOpen && <span style={{ color: 'white' }}>Inbox</span>}
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-pink-500/20" style={{ color: 'white' }}>
            <Calendar className="w-5 h-5" style={{ color: 'white' }} />
            {sidebarOpen && <span style={{ color: 'white' }}>Today</span>}
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-pink-500/20" style={{ color: 'white' }}>
            <Clock className="w-5 h-5" style={{ color: 'white' }} />
            {sidebarOpen && <span style={{ color: 'white' }}>Upcoming</span>}
          </a>

          <div className={`mt-6 ${sidebarOpen ? 'block' : 'hidden'}`}>
            <h3 className="px-3 text-xs font-semibold text-pink-100 uppercase tracking-wider mb-2" style={{ color: '#ffccdd' }}>Status</h3>
            <button 
              onClick={() => setActiveFilter('all')}
              className={`flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-pink-500/20 w-full text-left ${activeFilter === 'all' ? 'bg-pink-500/30' : ''}`}
              style={{ color: 'white' }}
            >
              <Inbox className="w-5 h-5" style={{ color: 'white' }} />
              <span style={{ color: 'white' }}>All</span>
            </button>
            <button 
              onClick={() => setActiveFilter('completed')}
              className={`flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-pink-500/20 w-full text-left ${activeFilter === 'completed' ? 'bg-pink-500/30' : ''}`}
              style={{ color: 'white' }}
            >
              <CheckCircle2 className="w-5 h-5" style={{ color: 'white' }} />
              <span style={{ color: 'white' }}>Completed</span>
            </button>
            <button 
              onClick={() => setActiveFilter('pending')}
              className={`flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-pink-500/20 w-full text-left ${activeFilter === 'pending' ? 'bg-pink-500/30' : ''}`}
              style={{ color: 'white' }}
            >
              <Circle className="w-5 h-5" style={{ color: 'white' }} />
              <span style={{ color: 'white' }}>Pending</span>
            </button>
          </div>
        </nav>

        {/* User Profile */}
        <div className="p-4 border-t border-pink-500/50 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-black text-sm font-medium" style={{ backgroundColor: 'white', color: 'black' }}>
              {user ? user.email.charAt(0).toUpperCase() : 'U'}
            </div>
            {sidebarOpen && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate" style={{ color: 'white' }}>{user ? user.email.split('@')[0] : 'User'}</p>
                <p className="text-xs text-pink-200 truncate" style={{ color: '#ffccdd' }}>{user ? user.email : 'user@example.com'}</p>
              </div>
            )}
            <button
              className="p-1 rounded hover:bg-pink-500/50 relative"
              onClick={() => setUserMenuOpen(!userMenuOpen)}
            >
              <MoreVertical className="w-4 h-4" style={{ color: 'white' }} />
            </button>
          </div>
          
          {/* User Menu Dropdown */}
          {userMenuOpen && (
            <div className="absolute bottom-full left-4 mb-2 w-48 bg-pink-600/90 backdrop-blur-sm border border-pink-500/50 rounded-2xl shadow-xl z-20 user-menu-container">
              <div className="py-1">
                <div className="px-4 py-2 text-xs font-medium text-pink-200 uppercase tracking-wider border-b border-pink-500/50">
                  Account
                </div>
                <button
                  onClick={() => {
                    // Open edit profile modal
                    setEditingName(user?.email.split('@')[0] || '');
                    setEditingEmail(user?.email || '');
                    setShowEditProfileModal(true);
                    setUserMenuOpen(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm hover:bg-pink-700/50 flex items-center gap-2 rounded-lg"
                  style={{ color: 'white' }}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit Profile
                </button>
                <button
                  onClick={() => {
                    signout();
                    router.push('/');
                    setUserMenuOpen(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm hover:bg-pink-700/50 flex items-center gap-2 rounded-lg"
                  style={{ color: 'white' }}
                >
                  <LogOut className="w-4 h-4" style={{ color: 'white' }} />
                  Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden md:ml-0">
        {/* Header */}
        <header className="border-b border-gray-300 bg-white" style={{ backgroundColor: 'white', borderBottom: '1px solid #d1d5db' }}>
          <div className="flex items-center justify-between p-4">
            <div>
              <h1 className="text-2xl font-semibold" style={{ color: 'black' }}>Good morning, {user ? user.email.split('@')[0] : 'User'}&apos;s Dashboard</h1>
              <p className="text-pink-500" style={{ color: '#ff69b4' }}>{formattedDate}</p>
            </div>

            <div className="flex items-center gap-4">
              {/* Mobile Search Icon */}
              <div className="md:hidden relative mobile-search-container">
                {mobileSearchOpen ? (
                  <div className="relative flex items-center">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-pink-400 w-4 h-4" style={{ color: 'black' }} />
                    <input
                      type="text"
                      placeholder="Search tasks..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent w-48"
                      style={{ borderColor: '#d1d5db', color: 'black' }}
                      autoFocus
                    />
                    {searchQuery && (
                      <button
                        onClick={() => setSearchQuery('')}
                        className="absolute right-8 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        style={{ color: 'black' }}
                      >
                        <X className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() => setMobileSearchOpen(false)}
                      className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      style={{ color: 'black' }}
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setMobileSearchOpen(true)}
                    className="p-2 rounded-lg bg-gray-100"
                  >
                    <Search className="w-5 h-5" style={{ color: 'black' }} />
                  </button>
                )}
              </div>

              {/* Desktop Search Bar */}
              <div className="hidden md:relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-pink-400 w-4 h-4" style={{ color: 'black' }} />
                <input
                  type="text"
                  placeholder="Search tasks..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  style={{ borderColor: '#d1d5db', color: 'black' }}
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                    style={{ color: 'black' }}
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              <button
                onClick={() => {
                  signout();
                  router.push('/');
                }}
                className="p-2 rounded-lg hover:bg-gray-100 hidden md:block"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.05)' }}
              >
                <LogOut className="w-5 h-5" style={{ color: 'black' }} />
              </button>
              
              {/* Mobile logout button */}
              <button
                onClick={() => {
                  signout();
                  router.push('/');
                }}
                className="p-2 rounded-lg hover:bg-gray-100 md:hidden"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.05)' }}
              >
                <LogOut className="w-5 h-5" style={{ color: 'black' }} />
              </button>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto p-6">
          {/* Add Task Input */}
          <div className="mb-8">
            <div className="flex gap-3">
              <input
                type="text"
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddTask()}
                placeholder="Add a new task..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                style={{ borderColor: '#d1d5db', color: 'black' }}
              />
              <select
                value={newTaskPriority}
                onChange={(e) => setNewTaskPriority(e.target.value as 'low' | 'medium' | 'high')}
                className="px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                style={{ borderColor: '#d1d5db', color: 'black', backgroundColor: 'white' }}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
              <button
                onClick={handleAddTask}
                className="px-4 py-3 text-white rounded-lg transition-colors flex items-center gap-2"
                style={{ backgroundColor: 'black' }}
              >
                <Plus className="w-4 h-4" />
                Add
              </button>
            </div>
          </div>

          {/* Tasks List */}
          <div className="space-y-2">
            <h2 className="text-lg font-medium mb-4" style={{ color: 'black' }}>Tasks</h2>

            {filteredTasks.length === 0 ? (
              <div className="text-center py-12">
                <div className="mx-auto w-24 h-24 bg-pink-100 rounded-full flex items-center justify-center mb-4" style={{ backgroundColor: 'rgba(255, 105, 180, 0.1)' }}>
                  <CheckCircle2 className="w-12 h-12 text-pink-400" style={{ color: '#ff69b4' }} />
                </div>
                <h3 className="text-lg font-medium text-pink-600 mb-1" style={{ color: 'black' }}>No tasks yet</h3>
                <p className="text-pink-500" style={{ color: '#ff69b4' }}>Add your first task to get started</p>
              </div>
            ) : (
              filteredTasks.map((task) => (
                <div
                  key={task.id}
                  className={`flex items-center gap-3 p-3 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors ${
                    task.completed ? 'opacity-70' : ''
                  }`}
                  style={{ borderColor: '#d1d5db' }}
                >
                  <button
                    onClick={() => toggleTaskCompletion(task.id)}
                    className="flex-shrink-0"
                  >
                    {task.completed ? (
                      <CheckCircle2 className="w-5 h-5 text-pink-500" style={{ color: '#ff69b4' }} />
                    ) : (
                      <Circle className="w-5 h-5 text-gray-400 hover:text-gray-600" style={{ color: 'black' }} />
                    )}
                  </button>

                  <div className="flex-1 min-w-0">
                    <p className={`truncate ${task.completed ? 'line-through text-gray-500' : ''}`}
                       style={{ color: task.completed ? 'black' : 'black' }}>
                      {task.title}
                    </p>
                    <div className="flex items-center gap-3 mt-1">
                      {task.priority && (
                        <span className={`inline-flex items-center gap-1 text-xs ${getPriorityColor(task.priority)}`}
                              style={{ color: task.priority === 'high' ? 'black' : task.priority === 'medium' ? '#ff69b4' : '#ff69b4' }}>
                          <Flag className={`w-3 h-3 ${task.priority === 'high' ? 'fill-black' : task.priority === 'medium' ? 'fill-pink-500' : 'fill-pink-400'}`} 
                                style={{ fill: task.priority === 'high' ? 'black' : task.priority === 'medium' ? '#ff69b4' : '#ff69b4' }} />
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                        </span>
                      )}
                      {task.dueDate && (
                        <span className="inline-flex items-center gap-1 text-xs text-pink-500" style={{ color: '#ff69b4' }}>
                          <Clock className="w-3 h-3" style={{ color: 'black' }} />
                          {formatDate(task.dueDate)}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="relative">
                    <button
                      onClick={() => toggleDropdown(task.id)}
                      className="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-50"
                      style={{ color: 'black' }}
                    >
                      <MoreVertical className="w-4 h-4" style={{ color: 'black' }} />
                    </button>

                    {openDropdown === task.id && (
                      <div className="absolute right-0 mt-1 w-48 bg-white border border-gray-300 rounded-lg shadow-lg z-10"
                           style={{ borderColor: '#d1d5db', backgroundColor: 'white' }}>
                        <div className="py-1">
                          <div className="px-3 py-2 text-xs font-medium text-pink-500 uppercase tracking-wider border-b border-gray-300"
                               style={{ color: '#ff69b4', borderColor: '#d1d5db' }}>
                            Set Priority
                          </div>
                          <button
                            onClick={() => updateTaskPriority(task.id, 'high')}
                            className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 flex items-center gap-2"
                            style={{ color: 'black' }}
                          >
                            <Flag className="w-4 h-4 text-black" style={{ color: 'black' }} />
                            High Priority
                          </button>
                          <button
                            onClick={() => updateTaskPriority(task.id, 'medium')}
                            className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 flex items-center gap-2"
                            style={{ color: '#ff69b4' }}
                          >
                            <Flag className="w-4 h-4 text-pink-500" style={{ color: '#ff69b4' }} />
                            Medium Priority
                          </button>
                          <button
                            onClick={() => updateTaskPriority(task.id, 'low')}
                            className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 flex items-center gap-2"
                            style={{ color: '#ff69b4' }}
                          >
                            <Flag className="w-4 h-4 text-pink-400" style={{ color: '#ff69b4' }} />
                            Low Priority
                          </button>
                          <div className="border-t border-gray-300" style={{ borderColor: '#d1d5db' }}></div>
                          <button
                            onClick={() => deleteTask(task.id)}
                            className="w-full text-left px-3 py-2 text-sm text-black hover:bg-gray-50 flex items-center gap-2"
                            style={{ color: 'black' }}
                          >
                            <X className="w-4 h-4" style={{ color: 'black' }} />
                            Delete Task
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </main>
      </div>

      {/* Right Sidebar - Mobile Overlay */}
      {mobileRightSidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 md:hidden"
          onClick={() => setMobileRightSidebarOpen(false)}
        ></div>
      )}

      {/* Right Sidebar */}
      {(rightSidebarOpen || mobileRightSidebarOpen) && (
        <div className={`${mobileRightSidebarOpen ? 'fixed inset-y-0 right-0 z-50' : 'hidden md:block'} w-80 bg-white border-l border-gray-300 p-4`} style={{ borderColor: '#d1d5db' }}>
          <div className="flex justify-between items-center mb-6">
            <h2 className="font-medium" style={{ color: 'black' }}>Quick Stats</h2>
            <button
              onClick={() => {
                if (window.innerWidth < 768) {
                  setMobileRightSidebarOpen(false);
                } else {
                  setRightSidebarOpen(false);
                }
              }}
              className="text-gray-400 hover:text-gray-600"
              style={{ color: 'black' }}
            >
              <ChevronDown className="w-4 h-4 rotate-90" />
            </button>
          </div>

          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-4" style={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}>
              <h3 className="text-sm font-medium text-pink-500 mb-2" style={{ color: '#ff69b4' }}>Today&apos;s Progress</h3>
              <div className="w-full bg-gray-300 rounded-full h-2" style={{ backgroundColor: '#d1d5db' }}>
                <div
                  className="bg-pink-500 h-2 rounded-full"
                  style={{ 
                    width: `${Math.min(100, (filteredTasks.filter(t => t.completed).length / filteredTasks.length) * 100)}%`,
                    backgroundColor: '#ff69b4'
                  }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1" style={{ color: 'black' }}>
                {filteredTasks.filter(t => t.completed).length} of {filteredTasks.length} completed
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4" style={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}>
              <h3 className="text-sm font-medium text-pink-500 mb-2" style={{ color: '#ff69b4' }}>Upcoming Deadlines</h3>
              <div className="space-y-3">
                {tasks
                  .filter(task => task.dueDate && !task.completed)
                  .sort((a, b) => new Date(a.dueDate!).getTime() - new Date(b.dueDate!).getTime())
                  .slice(0, 3)
                  .map(task => (
                    <div key={task.id} className="flex justify-between items-center">
                      <span className="text-sm truncate" style={{ color: 'black' }}>{task.title}</span>
                      <span className="text-xs text-gray-500" style={{ color: 'black' }}>{formatDate(task.dueDate!)}</span>
                    </div>
                  ))}
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4" style={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}>
              <h3 className="text-sm font-medium text-pink-500 mb-2" style={{ color: '#ff69b4' }}>Priority Distribution</h3>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm" style={{ color: 'black' }}>High Priority</span>
                  <span className="text-sm font-medium text-black" style={{ color: 'black' }}>
                    {tasks.filter(t => t.priority === 'high').length}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm" style={{ color: 'black' }}>Medium Priority</span>
                  <span className="text-sm font-medium text-pink-500" style={{ color: '#ff69b4' }}>
                    {tasks.filter(t => t.priority === 'medium').length}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm" style={{ color: 'black' }}>Low Priority</span>
                  <span className="text-sm font-medium text-pink-400" style={{ color: '#ff69b4' }}>
                    {tasks.filter(t => t.priority === 'low').length}
                  </span>
                </div>
              </div>
            </div>

            {/* Tasks grouped by priority */}
            <div className="bg-gray-50 rounded-lg p-4" style={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}>
              <h3 className="text-sm font-medium text-pink-500 mb-2" style={{ color: '#ff69b4' }}>Tasks by Priority</h3>
              <div className="space-y-3">
                {/* High Priority Tasks */}
                <div>
                  <h4 className="text-xs font-semibold text-black uppercase tracking-wider mb-1" style={{ color: 'black' }}>High Priority</h4>
                  <div className="space-y-1">
                    {tasks
                      .filter(task => task.priority === 'high' && !task.completed)
                      .map(task => (
                        <div key={task.id} className="text-sm truncate" style={{ color: 'black' }}>
                          {task.title}
                        </div>
                      ))}
                    {tasks.filter(task => task.priority === 'high' && !task.completed).length === 0 && (
                      <p className="text-xs text-gray-500 italic" style={{ color: 'black' }}>No high priority tasks</p>
                    )}
                  </div>
                </div>

                {/* Medium Priority Tasks */}
                <div>
                  <h4 className="text-xs font-semibold text-pink-500 uppercase tracking-wider mb-1" style={{ color: '#ff69b4' }}>Medium Priority</h4>
                  <div className="space-y-1">
                    {tasks
                      .filter(task => task.priority === 'medium' && !task.completed)
                      .map(task => (
                        <div key={task.id} className="text-sm truncate" style={{ color: 'black' }}>
                          {task.title}
                        </div>
                      ))}
                    {tasks.filter(task => task.priority === 'medium' && !task.completed).length === 0 && (
                      <p className="text-xs text-gray-500 italic" style={{ color: 'black' }}>No medium priority tasks</p>
                    )}
                  </div>
                </div>

                {/* Low Priority Tasks */}
                <div>
                  <h4 className="text-xs font-semibold text-pink-400 uppercase tracking-wider mb-1" style={{ color: '#ff69b4' }}>Low Priority</h4>
                  <div className="space-y-1">
                    {tasks
                      .filter(task => task.priority === 'low' && !task.completed)
                      .map(task => (
                        <div key={task.id} className="text-sm truncate" style={{ color: 'black' }}>
                          {task.title}
                        </div>
                      ))}
                    {tasks.filter(task => task.priority === 'low' && !task.completed).length === 0 && (
                      <p className="text-xs text-gray-500 italic" style={{ color: 'black' }}>No low priority tasks</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    {showEditProfileModal && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-2xl w-full max-w-md">
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold" style={{ color: 'black' }}>Edit Profile</h2>
              <button 
                onClick={() => setShowEditProfileModal(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1" style={{ color: 'black' }}>Name</label>
                <input
                  type="text"
                  value={editingName}
                  onChange={(e) => setEditingName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                  style={{ borderColor: '#d1d5db', color: 'black' }}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1" style={{ color: 'black' }}>Email</label>
                <input
                  type="email"
                  value={editingEmail}
                  onChange={(e) => setEditingEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                  style={{ borderColor: '#d1d5db', color: 'black' }}
                />
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowEditProfileModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                style={{ borderColor: '#d1d5db', color: 'black' }}
              >
                Cancel
              </button>
              <button
                onClick={async () => {
                  try {
                    // In a real application, you would make an API call to update the user profile
                    console.log('Updating user profile:', { name: editingName, email: editingEmail });
                    
                    // Here you would typically call an API to update the user profile
                    // const response = await api.put('/users/profile', { name: editingName, email: editingEmail });
                    
                    // For now, we'll simulate the update by updating the user in auth context
                    // In a real app, you would update the user object in the auth context
                    // after receiving a successful response from the backend
                    if (user) {
                      // Update the user in the auth context
                      updateUser({ email: editingEmail });
                    }
                    
                    // Close the modal after saving
                    setShowEditProfileModal(false);
                  } catch (error) {
                    console.error('Error updating profile:', error);
                    setError('Failed to update profile. Please try again.');
                  }
                }}
                className="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600"
                style={{ backgroundColor: '#ff69b4', color: 'white' }}
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    )}
    </div>
  );
};

export default Dashboard;