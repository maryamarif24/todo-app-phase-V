'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from './auth/auth-provider';
import Logo from "@/components/logo"

const Navbar: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    /* FIXES:
       1. fixed top-0 w-full: Keeps it at the top.
       2. z-50: Ensures it stays ABOVE the background image and other content.
       3. bg-white/80 + backdrop-blur: Gives a clean, consistent look across browsers.
    */
    <nav className="fixed top-0 left-0 w-full z-50 bg-white/70 backdrop-blur-md border-b border-pink-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            {/* Logo/App Name */}
            <Link href="/" className="flex-shrink-0 flex gap-3 items-center hover:opacity-80 transition-opacity">
              <Logo />
              {/* Using exact hex #db2777 for consistency */}
              <span className="text-2xl font-sans font-extrabold text-[#db2777]">Worksy Todo</span>
            </Link>
          </div>

          <div className="flex items-center">
            {/* Navigation Links */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              {isAuthenticated ? (
                <Link
                  href="/dashboard"
                  className="text-gray-700 hover:text-[#ec4899] px-3 py-2 rounded-md text-sm font-semibold transition-colors"
                >
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    href="/signin"
                    className="text-gray-600 hover:text-[#ec4899] px-3 py-2 rounded-md text-sm font-bold transition-colors"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="bg-[#ec4899] hover:bg-[#db2777] text-white px-5 py-2 rounded-full text-sm font-bold shadow-md shadow-pink-200 transition-all hover:scale-105"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;