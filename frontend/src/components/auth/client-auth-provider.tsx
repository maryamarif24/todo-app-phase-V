'use client';

import { AuthProvider } from './auth-provider';
import { ReactNode } from 'react';

export function ClientAuthProvider({ children }: { children: ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}
