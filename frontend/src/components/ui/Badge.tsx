/**
 * Badge — Label kecil untuk kategori & status.
 */

import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'safe' | 'warning' | 'danger' | 'info' | 'neutral';
  size?: 'sm' | 'md';
  className?: string;
}

const variantClasses: Record<string, string> = {
  safe:    'badge badge-safe',
  warning: 'badge badge-warning',
  danger:  'badge badge-danger',
  info:    'badge badge-info',
  neutral: 'badge badge-neutral',
};

export default function Badge({
  children,
  variant = 'neutral',
  size = 'md',
  className = '',
}: BadgeProps) {
  return (
    <span className={`${variantClasses[variant]} badge-${size} ${className}`}>
      {children}
    </span>
  );
}
