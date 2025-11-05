/**
 * KPI Card Component
 * Adapted from react-dashboard-theme/StatsCard.jsx
 * Now with TypeScript, Lucide icons, and Tailwind CSS
 */

'use client';

import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  percentage?: number;
  color?: 'blue' | 'green' | 'orange' | 'purple' | 'red';
  subtitle?: string;
  onClick?: () => void;
}

const colorClasses = {
  blue: 'bg-blue-500',
  green: 'bg-green-500',
  orange: 'bg-orange-500',
  purple: 'bg-purple-500',
  red: 'bg-red-500',
};

const trendColors = {
  up: 'text-green-600',
  down: 'text-red-600',
  neutral: 'text-gray-600',
};

export function KPICard({
  title,
  value,
  icon: Icon,
  trend = 'neutral',
  percentage,
  color = 'blue',
  subtitle,
  onClick,
}: KPICardProps) {
  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;

  return (
    <div
      className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 transition-all hover:shadow-md ${
        onClick ? 'cursor-pointer' : ''
      }`}
      onClick={onClick}
    >
      <div className="flex items-start justify-between mb-4">
        <div className={`${colorClasses[color]} p-3 rounded-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {percentage !== undefined && (
          <div className={`flex items-center gap-1 ${trendColors[trend]}`}>
            <TrendIcon className="w-4 h-4" />
            <span className="text-sm font-semibold">{percentage}%</span>
          </div>
        )}
      </div>

      <div>
        <p className="text-sm text-gray-600 mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
        {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
}
