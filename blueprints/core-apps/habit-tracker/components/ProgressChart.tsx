'use client';

import { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';

interface Habit {
  id: string;
  name: string;
  color: string;
  currentStreak: number;
  totalCompletions: number;
}

interface ProgressChartProps {
  habits: Habit[];
}

export default function ProgressChart({ habits }: ProgressChartProps) {
  const [selectedHabit, setSelectedHabit] = useState<string | 'all'>('all');

  // Mock weekly data (in production, this would come from API)
  const weeklyData = [
    { week: 'Week 1', completions: 18, target: 21 },
    { week: 'Week 2', completions: 22, target: 21 },
    { week: 'Week 3', completions: 19, target: 21 },
    { week: 'Week 4', completions: 24, target: 21 },
  ];

  // Streak comparison data
  const streakData = habits.map(habit => ({
    name: habit.name.length > 15 ? habit.name.substring(0, 12) + '...' : habit.name,
    current: habit.currentStreak,
    total: habit.totalCompletions,
  }));

  return (
    <div className="space-y-6">
      {/* Habit Selector */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          View Progress For
        </label>
        <select
          value={selectedHabit}
          onChange={e => setSelectedHabit(e.target.value)}
          className="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        >
          <option value="all">All Habits</option>
          {habits.map(habit => (
            <option key={habit.id} value={habit.id}>
              {habit.name}
            </option>
          ))}
        </select>
      </div>

      {/* Weekly Progress Chart */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Weekly Completion Rate
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={weeklyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="week" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="completions"
              stroke="#3B82F6"
              strokeWidth={2}
              name="Completions"
            />
            <Line
              type="monotone"
              dataKey="target"
              stroke="#10B981"
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Target"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Streak Comparison */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Current Streaks by Habit
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={streakData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="current" fill="#F59E0B" name="Current Streak" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Total Completions */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Total Completions
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={streakData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="total" fill="#8B5CF6" name="Total Completions" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white">
          <div className="text-sm font-medium mb-1">Avg Streak</div>
          <div className="text-3xl font-bold">
            {habits.length > 0
              ? Math.round(
                  habits.reduce((sum, h) => sum + h.currentStreak, 0) / habits.length
                )
              : 0}
          </div>
          <div className="text-xs opacity-80 mt-1">days</div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white">
          <div className="text-sm font-medium mb-1">Total Checks</div>
          <div className="text-3xl font-bold">
            {habits.reduce((sum, h) => sum + h.totalCompletions, 0)}
          </div>
          <div className="text-xs opacity-80 mt-1">completions</div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg p-6 text-white">
          <div className="text-sm font-medium mb-1">Active Habits</div>
          <div className="text-3xl font-bold">
            {habits.filter(h => h.currentStreak > 0).length}
          </div>
          <div className="text-xs opacity-80 mt-1">with streaks</div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white">
          <div className="text-sm font-medium mb-1">Consistency</div>
          <div className="text-3xl font-bold">
            {habits.length > 0
              ? Math.round(
                  (habits.filter(h => h.currentStreak >= 7).length / habits.length) * 100
                )
              : 0}
            %
          </div>
          <div className="text-xs opacity-80 mt-1">7+ day streaks</div>
        </div>
      </div>
    </div>
  );
}
