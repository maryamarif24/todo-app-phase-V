'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { saveAuthState, clearAuthState, type AuthState, type User, type Session } from '@/lib/auth-client';

interface AuthContextType extends AuthState {
  signin: (user: User, session: Session) => void;
  signout: () => void;
  updateUser: (updatedUser: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    session: null,
    isLoading: true,
    isAuthenticated: false,
  });

  // Load auth state from localStorage only on client
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const storedUser = localStorage.getItem('auth_user');
        const storedSession = localStorage.getItem('auth_session');

        if (storedUser && storedSession) {
          const user = JSON.parse(storedUser);
          const session = JSON.parse(storedSession);

          // Check if session has expired
          if (session.expires_at && new Date(session.expires_at) <= new Date()) {
            localStorage.removeItem('auth_user');
            localStorage.removeItem('auth_session');
            setAuthState({
              user: null,
              session: null,
              isLoading: false,
              isAuthenticated: false,
            });
          } else {
            setAuthState({
              user,
              session,
              isLoading: false,
              isAuthenticated: true,
            });
          }
        } else {
          setAuthState({
            user: null,
            session: null,
            isLoading: false,
            isAuthenticated: false,
          });
        }
      } catch (error) {
        console.error('Error loading auth state:', error);
        setAuthState({
          user: null,
          session: null,
          isLoading: false,
          isAuthenticated: false,
        });
      }
    }
  }, []);

  const signin = (user: User, session: Session) => {
    saveAuthState(user, session);
    setAuthState({
      user,
      session,
      isLoading: false,
      isAuthenticated: true,
    });
  };

  const signout = () => {
    clearAuthState();
    setAuthState({
      user: null,
      session: null,
      isLoading: false,
      isAuthenticated: false,
    });
  };

  const updateUser = (updatedUser: Partial<User>) => {
    if (authState.user) {
      const newUser = { ...authState.user, ...updatedUser };
      const newSession = authState.session ? { ...authState.session } : null;

      if (newSession) {
        saveAuthState(newUser, newSession);
      }

      setAuthState({
        user: newUser,
        session: newSession,
        isLoading: false,
        isAuthenticated: true,
      });
    }
  };

  return (
    <AuthContext.Provider value={{ ...authState, signin, signout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
