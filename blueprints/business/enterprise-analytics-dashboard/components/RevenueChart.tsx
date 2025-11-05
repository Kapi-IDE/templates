/**
 * Revenue Chart Component
 * Adapted from react-dashboard-theme/ChartCard.jsx
 * Now using Recharts with TypeScript
 */

'use client';

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Download, Filter } from 'lucide-react';

interface ChartData {
  name: string;
  value: number;
  [key: string]: string | number;
}

interface RevenueChartProps {
  title: string;
  subtitle?: string;
  data: ChartData[];
  chartType?: 'line' | 'bar' | 'area';
  dataKeys: string[];
  colors?: string[];
  height?: number;
  onExport?: () => void;
  onFilter?: () => void;
}

export function RevenueChart({
  title,
  subtitle,
  data,
  chartType = 'line',
  dataKeys,
  colors = ['#3b82f6', '#10b981', '#f59e0b'],
  height = 350,
  onExport,
  onFilter,
}: RevenueChartProps) {
  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 5, right: 30, left: 20, bottom: 5 },
    };

    const axes = (
      <>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="name" stroke="#6b7280" />
        <YAxis stroke="#6b7280" />
        <Tooltip />
        <Legend />
      </>
    );

    switch (chartType) {
      case 'bar':
        return (
          <BarChart {...commonProps}>
            {axes}
            {dataKeys.map((key, idx) => (
              <Bar key={key} dataKey={key} fill={colors[idx % colors.length]} />
            ))}
          </BarChart>
        );
      case 'area':
        return (
          <AreaChart {...commonProps}>
            {axes}
            {dataKeys.map((key, idx) => (
              <Area
                key={key}
                type="monotone"
                dataKey={key}
                stroke={colors[idx % colors.length]}
                fill={colors[idx % colors.length]}
                fillOpacity={0.6}
              />
            ))}
          </AreaChart>
        );
      default:
        return (
          <LineChart {...commonProps}>
            {axes}
            {dataKeys.map((key, idx) => (
              <Line
                key={key}
                type="monotone"
                dataKey={key}
                stroke={colors[idx % colors.length]}
                strokeWidth={2}
              />
            ))}
          </LineChart>
        );
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {subtitle && <p className="text-sm text-gray-600 mt-1">{subtitle}</p>}
        </div>
        <div className="flex gap-2">
          {onFilter && (
            <button
              onClick={onFilter}
              className="px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition flex items-center gap-2"
            >
              <Filter className="w-4 h-4" />
              Filter
            </button>
          )}
          {onExport && (
            <button
              onClick={onExport}
              className="px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export
            </button>
          )}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={height}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
}
