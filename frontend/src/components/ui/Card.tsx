/**
 * Card — Komponen kartu glassmorphism reusable.
 */

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'glass' | 'elevated' | 'danger';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  onClick?: () => void;
  id?: string;
  style?: React.CSSProperties;
}

const variantClasses: Record<string, string> = {
  default:  'card',
  glass:    'card card-glass',
  elevated: 'card card-elevated',
  danger:   'card card-danger',
};

const paddingClasses: Record<string, string> = {
  none: '',
  sm:   'card-padding-sm',
  md:   'card-padding-md',
  lg:   'card-padding-lg',
};

export default function Card({
  children,
  className = '',
  variant = 'default',
  padding = 'md',
  onClick,
  id,
  style,
}: CardProps) {
  return (
    <div
      id={id}
      className={`${variantClasses[variant]} ${paddingClasses[padding]} ${className}`}
      style={style}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      {children}
    </div>
  );
}
