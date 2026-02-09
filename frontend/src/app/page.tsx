'use client';

import Link from 'next/link';
import { useAuth } from '@/components/auth/auth-provider';

export default function Home() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#ec4899]"></div>
      </div>
    );
  }

  return (
    /* FIX: We use a pseudo-element or a dual background to "fade" the dark pink image */
    <div className="relative min-h-screen w-full overflow-x-hidden">

      {/* Background Layer with Opacity Control */}
      <div
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('/bg.jpg')",
        }}
      />

      {/* TRANSPARENT OVERLAY:
         This is the magic part. It tints the dark image to a light,
         cleaner version so your pink text is actually readable.
      */}
      <div className="absolute inset-0 z-0 bg-white/80 backdrop-blur-[2px]" />


      {/* HERO SECTION */}
      <section className="relative w-full pt-24 lg:pt-32 pb-20 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

            {/* LEFT SIDE: TEXT CONTENT */}
            <div className="relative z-10">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-pink-50 border border-pink-100 mb-6 shadow-sm">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-pink-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-pink-500"></span>
                </span>
                <span className="text-xs font-bold text-[#db2777] uppercase tracking-wider">Productivity Redefined</span>
              </div>

              <h1 className="text-4xl tracking-tight font-black text-gray-900 sm:text-5xl md:text-6xl leading-[1.1]">
                <span className="block text-[#db2777]">Streamline Your Tasks with</span>
                <span className="block text-gray-800">Worksy Todo</span>
              </h1>
              <p className="mt-6 text-lg text-gray-600 max-w-xl leading-relaxed font-medium">
                A professional task management suite designed for clarity.
                Organize work, track progress, and hit deadlines with a minimalist interface.
              </p>

              <div className="mt-10 flex flex-col sm:flex-row gap-4">
                <Link
                  href="/signup"
                  className="flex items-center justify-center px-10 py-4 text-white bg-[#ec4899] hover:bg-[#db2777] rounded-xl font-bold text-lg shadow-xl shadow-pink-200 transition-all hover:-translate-y-1 active:scale-95"
                >
                  Get Started Free
                </Link>
                <Link
                  href="/signin"
                  className="flex items-center justify-center px-10 py-4 border-2 border-gray-200 text-gray-700 bg-white hover:bg-gray-50 rounded-xl font-bold text-lg shadow-sm transition-all hover:-translate-y-1"
                >
                  Sign In
                </Link>
              </div>
            </div>

            {/* RIGHT SIDE: GLASS ELEMENTS */}
            <div className="relative h-[500px] w-full hidden lg:flex items-center justify-center">
              <div className="absolute w-[500px] h-[500px] bg-gradient-to-r from-pink-200/30 to-indigo-100/20 rounded-full blur-[120px]" />

              {/* Main Task Card */}
              <div className="absolute z-20 w-72 h-48 bg-white/40 backdrop-blur-2xl border border-white/60 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.08)] p-6 animate-float">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 rounded-lg bg-[#ec4899] flex items-center justify-center text-white shadow-lg">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7"/></svg>
                  </div>
                  <div className="h-2 w-20 bg-gray-200/50 rounded-full" />
                </div>
                <div className="space-y-3">
                  <div className="h-3 w-full bg-white/60 rounded-full" />
                  <div className="h-3 w-3/4 bg-white/60 rounded-full" />
                </div>
              </div>

              {/* High Priority Tag */}
              <div className="absolute top-10 right-10 z-30 w-36 h-14 bg-white/70 backdrop-blur-lg border border-white/80 rounded-2xl shadow-xl flex items-center justify-center space-x-2 animate-float-delayed">
                <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
                <span className="text-xs font-bold text-gray-700 uppercase tracking-tighter">High Priority</span>
              </div>

              {/* Calendar Glass */}
              <div className="absolute -bottom-5 left-10 z-10 w-40 h-40 bg-white/30 backdrop-blur-md border border-white/40 rounded-[2rem] rotate-[-15deg] flex flex-col p-4 shadow-lg opacity-90">
                <div className="h-4 w-full border-b border-white/40 mb-3" />
                <div className="grid grid-cols-4 gap-2">
                  {[...Array(8)].map((_, i) => (
                    <div key={i} className="h-4 w-4 bg-white/40 rounded-sm" />
                  ))}
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* FEATURES SECTION (Pure White Background) */}
      <div className="relative z-10 bg-white py-24 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-[#ec4899] font-bold uppercase tracking-widest text-sm">Framework</h2>
            <p className="text-3xl md:text-4xl font-black text-gray-900 mt-2">Built for Performance</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard title="Prioritize" desc="Filter by urgency." />
            <FeatureCard title="Schedule" desc="Sync with due dates." />
            <FeatureCard title="Categorize" desc="Group with smart tags." />
            <FeatureCard title="Automate" desc="Set recurring loops." />
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(1deg); }
        }
        @keyframes float-delayed {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(15px) rotate(-2deg); }
        }
        .animate-float { animation: float 6s ease-in-out infinite; }
        .animate-float-delayed { animation: float-delayed 8s ease-in-out infinite; }
      `}</style>
    </div>
  );
}

function FeatureCard({ title, desc }: { title: string, desc: string }) {
  return (
    <div className="group p-8 rounded-2xl bg-[#fafafa] border border-gray-100 hover:border-pink-200 hover:bg-white hover:shadow-xl transition-all duration-300">
      <div className="h-10 w-10 bg-white shadow-sm border border-gray-100 text-[#ec4899] rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
      </div>
      <h3 className="text-lg font-bold text-gray-900">{title}</h3>
      <p className="text-sm text-gray-500 mt-2">{desc}</p>
    </div>
  );
}