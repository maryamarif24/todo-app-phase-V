'use client';

import { useState, useRef, useEffect } from 'react';
import { api } from '@/lib/api';
import { useAuth } from '@/components/auth/auth-provider';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface Conversation {
  id: string;
  messages: Message[];
}

export default function FloatingChatWidget() {
  const { user, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([
    { id: 'floating-chat', messages: [] } // Single conversation for the floating widget
  ]);
  const [currentConversationId] = useState<string>('floating-chat'); // Fixed ID for floating widget
  const [error, setError] = useState('');
  const [showAuthPrompt, setShowAuthPrompt] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [conversations, currentConversationId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Initialize with an empty conversation when user authenticates
  useEffect(() => {
    if (isAuthenticated && user) {
      // Reset conversation when user authenticates
      setConversations([{ id: 'floating-chat', messages: [] }]);
    }
  }, [isAuthenticated, user]);

  const getCurrentConversation = () => {
    // Get the fixed conversation for the floating widget
    return conversations.find(conv => conv.id === currentConversationId);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading || !user) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    // Add user message to current conversation (local only for UI)
    setConversations(prev =>
      prev.map(conv =>
        conv.id === currentConversationId
          ? { ...conv, messages: [...conv.messages, userMessage] }
          : conv
      )
    );

    setInputValue('');
    setIsLoading(true);
    setError('');

    try {
      // Send message to backend API using the new todo-operation endpoint
      // This endpoint doesn't store conversation history in the database
      const response = await api.post<{
        response: string;
        timestamp: string;
      }>('/chat/todo-operation', {
        message: inputValue,
      });

      if (response.error) {
        setError(response.error);
        return;
      }

      if (response.data) {
        const aiMessage: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: response.data.response,
          timestamp: response.data.timestamp,
        };

        // Update conversation with AI response (local only)
        setConversations(prev =>
          prev.map(conv =>
            conv.id === currentConversationId
              ? { ...conv, messages: [...conv.messages, aiMessage] }
              : conv
          )
        );
      }
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    if (!isAuthenticated) {
      setShowAuthPrompt(true);
      setTimeout(() => setShowAuthPrompt(false), 3000); // Hide after 3 seconds
      return;
    }
    setIsOpen(!isOpen);
  };

  const currentConv = getCurrentConversation();

  return (
    <>
      {/* Floating Chat Icon */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={toggleChat}
          className="w-14 h-14 rounded-full bg-pink-500 text-white flex items-center justify-center shadow-lg hover:bg-pink-600 transition-all duration-300 transform hover:scale-110"
          aria-label="Open chat"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </button>
      </div>

      {/* Authentication Prompt */}
      {showAuthPrompt && (
        <div className="fixed bottom-24 right-6 z-50 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg animate-fadeInOut">
          Please sign in to use the chat feature.
        </div>
      )}

      {/* Chat Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-30">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md max-h-[80vh] flex flex-col">
            {/* Header */}
            <div
              className="p-4 border-b flex justify-between items-center rounded-t-3xl"
              style={{
                background: 'linear-gradient(135deg, #ff6b9d 0%, #c44569 100%)',
                color: 'white'
              }}
            >
              <h2 className="text-lg font-bold">Todo Assistant</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="text-white hover:text-pink-100"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {!isAuthenticated ? (
                <div className="text-center py-8 text-gray-500">
                  <p>Please sign in to use the chat feature.</p>
                </div>
              ) : currentConv && currentConv.messages.length > 0 ? (
                currentConv.messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-3xl p-3 ${
                        message.role === 'user'
                          ? 'bg-pink-500 text-white rounded-br-none'
                          : 'bg-pink-100 text-pink-800 rounded-bl-none'
                      }`}
                    >
                      <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                      <div
                        className={`text-xs mt-1 ${
                          message.role === 'user' ? 'text-pink-100' : 'text-pink-600'
                        }`}
                      >
                        {new Date(message.timestamp).toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500">
                  <div className="text-center">
                    <div className="text-4xl mb-2">💬</div>
                    <h3 className="font-medium">Start a conversation</h3>
                    <p className="text-sm mt-1">Ask me to help manage your todos!</p>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t p-3 bg-pink-50 rounded-b-3xl">
              {error && (
                <div className="mb-2 p-2 bg-red-100 text-red-700 rounded-xl text-sm">
                  {error}
                </div>
              )}
              <div className="flex gap-2">
                <input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about your todos..."
                  className="flex-1 border border-pink-300 rounded-2xl px-4 py-2 focus:outline-none focus:ring-2 text-sm"
                  style={{
                    '--tw-ring-color': '#ff6b9d'
                  } as React.CSSProperties}
                  disabled={isLoading || !isAuthenticated}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !inputValue.trim() || !isAuthenticated}
                  className="px-4 py-2 bg-pink-500 text-white rounded-2xl hover:bg-pink-600 disabled:opacity-50 transition text-sm"
                >
                  {isLoading ? (
                    <svg
                      className="animate-spin h-4 w-4 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                  ) : (
                    'Send'
                  )}
                </button>
              </div>
              <div className="mt-1 text-xs text-pink-500 text-center">
                Ask me to add, complete, or manage your todos
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}