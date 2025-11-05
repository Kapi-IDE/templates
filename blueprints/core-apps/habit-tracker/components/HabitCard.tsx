'use client';

import { Check, Flame, Trophy, Calendar } from 'lucide-react';
import { format } from 'date-fns';

interface HabitCardProps {
  habit: {
    id: string;
    name: string;
    description?: string;
    color: string;
    icon?: string;
    targetDays: number;
    currentStreak: number;
    longestStreak: number;
    isCompletedToday: boolean;
    totalCompletions: number;
  };
  onToggle: () => void;
}

export default function HabitCard({ habit, onToggle }: HabitCardProps) {
  return (
    <div
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
      style={{ borderTop: `4px solid ${habit.color}` }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {habit.icon && <span className="mr-2">{habit.icon}</span>}
            {habit.name}
          </h3>
          {habit.description && (
            <p className="text-sm text-gray-600">{habit.description}</p>
          )}
        </div>

        {/* Completion Button */}
        <button
          onClick={onToggle}
          className={`flex items-center justify-center w-12 h-12 rounded-full transition-all ${
            habit.isCompletedToday
              ? 'bg-green-500 text-white shadow-lg scale-110'
              : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
          }`}
        >
          <Check size={24} strokeWidth={3} />
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        {/* Current Streak */}
        <div className="bg-orange-50 rounded-lg p-3 text-center">
          <Flame
            size={20}
            className={`mx-auto mb-1 ${
              habit.currentStreak > 0 ? 'text-orange-500' : 'text-gray-400'
            }`}
          />
          <div className="text-2xl font-bold text-gray-900">{habit.currentStreak}</div>
          <div className="text-xs text-gray-600">day streak</div>
        </div>

        {/* Longest Streak */}
        <div className="bg-purple-50 rounded-lg p-3 text-center">
          <Trophy size={20} className="mx-auto mb-1 text-purple-500" />
          <div className="text-2xl font-bold text-gray-900">{habit.longestStreak}</div>
          <div className="text-xs text-gray-600">best</div>
        </div>

        {/* Total Completions */}
        <div className="bg-blue-50 rounded-lg p-3 text-center">
          <Calendar size={20} className="mx-auto mb-1 text-blue-500" />
          <div className="text-2xl font-bold text-gray-900">{habit.totalCompletions}</div>
          <div className="text-xs text-gray-600">total</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-2">
        <div className="flex justify-between text-xs text-gray-600 mb-1">
          <span>Weekly goal</span>
          <span>{Math.min(habit.currentStreak, habit.targetDays)}/{habit.targetDays} days</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all"
            style={{
              width: `${Math.min((habit.currentStreak / habit.targetDays) * 100, 100)}%`,
              backgroundColor: habit.color,
            }}
          />
        </div>
      </div>

      {/* Status */}
      {habit.isCompletedToday ? (
        <div className="text-sm text-green-600 font-medium flex items-center gap-1">
          <Check size={16} />
          Completed today!
        </div>
      ) : (
        <div className="text-sm text-gray-500">Not done yet today</div>
      )}
    </div>
  );
}
