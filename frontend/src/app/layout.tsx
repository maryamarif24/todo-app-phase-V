import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ClientAuthProvider } from '@/components/auth/client-auth-provider';
import FloatingChatWidget from '@/components/FloatingChatWidget';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Worksy Todo',
  description: 'Full-stack web todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ClientAuthProvider>
          {children}
          <FloatingChatWidget />
        </ClientAuthProvider>
      </body>
    </html>
  );
}
