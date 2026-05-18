import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        danger:  '#ef4444',
        warning: '#f59e0b',
        safe:    '#22c55e',
      },
    },
  },
  plugins: [],
};

export default config;
