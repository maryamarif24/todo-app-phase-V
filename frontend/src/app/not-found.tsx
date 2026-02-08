import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">404 - Page Not Found</h2>
      <p className="text-gray-600 mb-4">
        Could not find the requested page.
      </p>
      <Link
        href="/"
        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Return Home
      </Link>
    </div>
  );
}