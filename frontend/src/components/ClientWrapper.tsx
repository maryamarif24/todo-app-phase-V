'use client';

import { ReactNode, useEffect, useState } from 'react';
import { ClientAuthProvider } from '@/components/auth/client-auth-provider';
import FloatingChatWidget from '@/components/FloatingChatWidget';
import ConditionalNavbar from '@/components/ConditionalNavbar';

export default function ClientWrapper({ children }: { children: ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    // Render loading state on server to prevent hydration mismatch
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-pink-500"></div>
      </div>
    );
  }

  return (
    <ClientAuthProvider>
      <ConditionalNavbar />
      <main>
        {children}
      </main>
      <FloatingChatWidget />
    </ClientAuthProvider>
  );
}
