'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, X, Minimize2 } from 'lucide-react';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface ChatWidgetProps {
  onTaskCreated?: (task: any) => void;
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({ onTaskCreated }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hi! I'm your AI assistant. I can help you create, update, and manage your tasks. Try saying 'Create a task to buy groceries' or 'Show me my pending tasks'.",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // Simulate AI processing
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Simple command parsing (in a real app, this would call your backend AI)
      const command = inputValue.toLowerCase();

      let response = '';

      if (command.includes('create') && command.includes('task')) {
        // Extract task title from message
        const taskMatch = inputValue.match(/create a task to (.+)/i) ||
                         inputValue.match(/create task (.+)/i) ||
                         inputValue.match(/add task (.+)/i);

        if (taskMatch) {
          const taskTitle = taskMatch[1];
          response = `I've created a new task: "${taskTitle}". You can find it in your dashboard.`;

          // Notify parent component about new task
          if (onTaskCreated) {
            onTaskCreated({
              title: taskTitle,
              priority: 'medium'
            });
          }
        } else {
          response = 'I need a task title. Try: "Create a task to buy groceries"';
        }
      } else if (command.includes('show') && command.includes('task')) {
        response = 'You can see all your tasks in the dashboard. I can help you filter them by saying "show completed tasks" or "show pending tasks".';
      } else if (command.includes('help')) {
        response = 'I can help you:\n• Create tasks: "Create a task to [description]"\n• View tasks: "Show my tasks"\n• Mark complete: "Mark [task] as complete"\n• Set priority: "Set [task] to high priority"';
      } else {
        response = "I'm not sure how to help with that. Try asking me to create a task or check the help command.";
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response,
        isUser: false,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(true)}
          className="bg-pink-500 hover:bg-pink-600 text-white rounded-full p-4 shadow-lg transition-all duration-200 hover:scale-110"
          style={{ backgroundColor: '#ff69b4' }}
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className={`bg-white rounded-2xl shadow-2xl border border-gray-200 transition-all duration-200 ${
        isMinimized ? 'h-14' : 'h-96'
      } w-80 flex flex-col overflow-hidden`} style={{ backgroundColor: 'white' }}>

        {/* Header */}
        <div className="bg-pink-500 text-white p-4 rounded-t-2xl flex items-center justify-between" style={{ backgroundColor: '#ff69b4' }}>
          <div className="flex items-center gap-2">
            <MessageCircle className="w-5 h-5" />
            <span className="font-medium">AI Assistant</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="hover:bg-pink-600 rounded p-1 transition-colors"
              style={{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }}
            >
              <Minimize2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="hover:bg-pink-600 rounded p-1 transition-colors"
              style={{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {!isMinimized && (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                      message.isUser
                        ? 'bg-pink-500 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                    style={{
                      backgroundColor: message.isUser ? '#ff69b4' : 'rgba(0, 0, 0, 0.05)',
                      color: message.isUser ? 'white' : 'black'
                    }}
                  >
                    <div className="whitespace-pre-line">{message.text}</div>
                    <div className={`text-xs mt-1 ${
                      message.isUser ? 'text-pink-100' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-2xl px-4 py-2" style={{ backgroundColor: 'rgba(0, 0, 0, 0.05)' }}>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200" style={{ borderColor: '#d1d5db' }}>
              <div className="flex gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your message..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  style={{ borderColor: '#d1d5db', color: 'black' }}
                  disabled={isTyping}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isTyping}
                  className="bg-pink-500 hover:bg-pink-600 text-white rounded-full p-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{ backgroundColor: '#ff69b4' }}
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
