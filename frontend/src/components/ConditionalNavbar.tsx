'use client';

import { usePathname } from 'next/navigation';
import Navbar from '@/components/Navbar';

const ConditionalNavbar = () => {
  const pathname = usePathname();

  // Don't show the default navbar on dashboard pages
  if (pathname.startsWith('/dashboard')) {
    return null;
  }

  return <Navbar />;
};

export default ConditionalNavbar;
