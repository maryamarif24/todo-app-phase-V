'use client';

import { useState, useRef, useEffect } from 'react';
import { api } from '@/lib/api';
import { useAuth } from '@/components/auth/auth-provider';
import { Send, X, MessageSquare } from 'lucide-react';

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
    { id: 'floating-chat', messages: [] }
  ]);
  const [currentConversationId] = useState<string>('floating-chat');
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

  // Reset conversation when user authenticates
  useEffect(() => {
    if (isAuthenticated && user) {
      setConversations([{ id: 'floating-chat', messages: [] }]);
    }
  }, [isAuthenticated, user]);

  const getCurrentConversation = () => {
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

    setConversations(prev =>
      prev.map(conv =>
        conv.id === currentConversationId
          ? { ...conv, messages: [...conv.messages, userMessage] }
          : conv
      )
    );

    const messageToSend = inputValue;
    setInputValue('');
    setIsLoading(true);
    setError('');

    try {
      const response = await api.post<{
        response: string;
        timestamp: string;
      }>('/chat/todo-operation', {
        message: messageToSend,
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

        setConversations(prev =>
          prev.map(conv =>
            conv.id === currentConversationId
              ? { ...conv, messages: [...conv.messages, aiMessage] }
              : conv
          )
        );

        const responseText = response.data.response.toLowerCase();
        if (
          responseText.includes('[success]') ||
          responseText.includes('created') ||
          responseText.includes('added') ||
          responseText.includes('deleted') ||
          responseText.includes('removed') ||
          responseText.includes('completed') ||
          responseText.includes('marked as') ||
          responseText.includes('updated') ||
          responseText.includes('todo') ||
          responseText.includes('task')
        ) {
          // Dispatch event to refresh tasks in dashboard
          window.dispatchEvent(new CustomEvent('refreshTasks'));
        }
      }
    } catch (err) {
      setError('Failed to send message. Please try again.');
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
      setTimeout(() => setShowAuthPrompt(false), 3000);
      return;
    }
    setIsOpen(!isOpen);
  };

  const currentConv = getCurrentConversation();

  return (
    <>
      {/* Floating Chat Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={toggleChat}
          className="w-14 h-14 rounded-full bg-[#ec4899] text-white flex items-center justify-center shadow-[0_8px_25px_rgba(236,72,153,0.4)] hover:bg-[#db2777] transition-all duration-300 transform hover:scale-110 active:scale-95"
        >
          <MessageSquare className="w-6 h-6" />
        </button>
      </div>

      {/* Auth Prompt Toast */}
      {showAuthPrompt && (
        <div className="fixed bottom-24 right-6 z-50 bg-gray-900/90 backdrop-blur-md text-white px-6 py-3 rounded-2xl shadow-xl animate-in fade-in slide-in-from-bottom-4">
          <p className="text-sm font-bold">Please sign in to use the assistant</p>
        </div>
      )}

      {/* Chat Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20 backdrop-blur-sm animate-in fade-in duration-300">
          <div className="bg-white rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.15)] w-full max-w-md h-[600px] max-h-[85vh] flex flex-col overflow-hidden border border-white/20">

            {/* Header */}
            <div className="p-6 bg-gradient-to-r from-[#ec4899] to-[#db2777] text-white flex justify-between items-center shadow-md">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-white/20 rounded-xl backdrop-blur-md">
                  <MessageSquare className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-lg font-black tracking-tight">Todo Assistant</h2>
              </div>
              <button onClick={() => setIsOpen(false)} className="p-2 hover:bg-white/10 rounded-full transition-colors">
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50/50">
              {currentConv && currentConv.messages.length > 0 ? (
                currentConv.messages.map((message) => (
                  <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2`}>
                    <div className={`max-w-[85%] rounded-[1.5rem] px-4 py-3 shadow-sm ${
                        message.role === 'user'
                          ? 'bg-[#ec4899] text-white rounded-br-none'
                          : 'bg-white border border-pink-100 text-gray-800 rounded-bl-none'
                      }`}>
                      <p className="text-sm leading-relaxed font-medium">{message.content}</p>
                      <span className={`text-[10px] mt-2 block opacity-70 font-bold ${message.role === 'user' ? 'text-white' : 'text-pink-500'}`}>
                        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-40">
                  <div className="w-20 h-20 bg-pink-100 rounded-full flex items-center justify-center">
                    <MessageSquare className="w-10 h-10 text-pink-500" />
                  </div>
                  <div>
                    <h3 className="font-black text-gray-900">Start a conversation</h3>
                    <p className="text-sm text-gray-500">Ask me to add or manage your tasks!</p>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-6 bg-white border-t border-gray-100">
              {error && (
                <div className="mb-3 p-3 bg-red-50 text-red-600 rounded-xl text-xs font-bold border border-red-100">
                  {error}
                </div>
              )}
              <div className="flex gap-2 relative">
                <input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type a task..."
                  /* FIX: text-pink-700 ensures dark pink typing color */
                  className="flex-1 bg-gray-50 border border-gray-200 rounded-2xl px-5 py-3 focus:outline-none focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 text-sm font-bold text-pink-700 placeholder-pink-300 transition-all"
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !inputValue.trim()}
                  className="p-3 bg-[#ec4899] text-white rounded-2xl hover:bg-[#db2777] disabled:opacity-50 transition-all shadow-lg shadow-pink-100 active:scale-95"
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
              <p className="mt-3 text-[10px] text-pink-400 text-center font-black uppercase tracking-widest">
                AI Productivity Powered
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}