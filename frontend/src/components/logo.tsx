/**
 * Logo component for Worksy Todo App
 * A modern checkmark logo representing task completion
 *
 * LOGO CONCEPT:
 * - Rounded square background with pink gradient
 * - Centered circular outline in white
 * - Bold checkmark overlapping the circle
 * - Minimal, clean, productivity-focused design
 *
 * COLORS:
 * - Gradient: #FFB6C1 (light pink) → #FF1493 (deep magenta)
 * - Foreground: White (#FFFFFF)
 *
 * USAGE:
 * - Works on light and dark backgrounds
 * - Scalable from 32x32 to any size
 * - Icon-only or with text
 */

export default function Logo({ className = "", size = 40 }: { className?: string; size?: number }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Gradient definition */}
      <defs>
        <linearGradient id="pinkGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#FFB6C1" />
          <stop offset="100%" stopColor="#FF1493" />
        </linearGradient>
      </defs>

      {/* Rounded square background */}
      <rect
        x="4"
        y="4"
        width="56"
        height="56"
        rx="14"
        fill="url(#pinkGradient)"
      />

      {/* Centered circular outline */}
      <circle
        cx="32"
        cy="32"
        r="18"
        fill="none"
        stroke="white"
        strokeWidth="3"
      />

      {/* Bold checkmark */}
      <path
        d="M22 32 L29 39 L42 26"
        fill="none"
        stroke="white"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
