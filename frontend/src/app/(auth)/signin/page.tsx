'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { SigninForm } from '@/components/auth/signin-form';
import Link from 'next/link';
import { useAuth } from '@/components/auth/auth-provider';

export default function SigninPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  // Redirect to todos if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h1 className="text-2xl font-bold text-center mb-6" style={{ color: "#7F1734" }}>Sign In</h1>
      <SigninForm />
      <p className="mt-4 text-center text-sm" style={{ color: "#7F1734" }}>
        Don&apos;t have an account?{' '}
        <Link href="/signup" className="text-blue-600 hover:underline">
          Sign up
        </Link>
      </p>
    </div>
  );
}
