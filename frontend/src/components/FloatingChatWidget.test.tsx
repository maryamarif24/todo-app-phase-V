import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import FloatingChatWidget from '@/components/FloatingChatWidget';

// Mock the auth context
jest.mock('@/components/auth/auth-provider', () => ({
  useAuth: () => ({
    user: { id: 'test-user-id', email: 'test@example.com' },
    isAuthenticated: true,
  }),
}));

// Mock the API module
jest.mock('@/lib/api', () => ({
  api: {
    post: jest.fn(() => Promise.resolve({ data: { response: 'Test response', conversation_id: 'test-conversation-id', timestamp: '2023-01-01T00:00:00Z' } })),
  },
}));

describe('FloatingChatWidget', () => {
  it('renders the floating chat icon', () => {
    render(<FloatingChatWidget />);
    
    // Check if the chat icon button is present
    const chatIcon = screen.getByLabelText(/Open chat/i);
    expect(chatIcon).toBeInTheDocument();
  });

  it('opens the chat modal when icon is clicked', () => {
    render(<FloatingChatWidget />);
    
    // Click the chat icon
    const chatIcon = screen.getByLabelText(/Open chat/i);
    fireEvent.click(chatIcon);
    
    // Check if the chat modal is open
    const chatModal = screen.getByText(/Todo Assistant/i);
    expect(chatModal).toBeInTheDocument();
  });

  it('closes the chat modal when close button is clicked', () => {
    render(<FloatingChatWidget />);
    
    // Open the chat first
    const chatIcon = screen.getByLabelText(/Open chat/i);
    fireEvent.click(chatIcon);
    
    // Then click the close button
    const closeButton = screen.getByLabelText(/close/i);
    fireEvent.click(closeButton);
    
    // Check if the chat modal is closed
    const chatModal = screen.queryByText(/Todo Assistant/i);
    expect(chatModal).not.toBeInTheDocument();
  });
});