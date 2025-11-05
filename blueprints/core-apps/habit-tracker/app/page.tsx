'use client';

/**
 * Habit Tracker - Main Page
 * Features: Habit list, quick check-ins, streak display, charts
 */

import { useState, useEffect } from 'react';
import { Check, Plus, TrendingUp, Calendar, Target, Flame } from 'lucide-react';
import { format, startOfDay } from 'date-fns';
import HabitCard from '@/components/HabitCard';
import HabitForm from '@/components/HabitForm';
import StatsOverview from '@/components/StatsOverview';
import ProgressChart from '@/components/ProgressChart';

interface Habit {
  id: string;
  name: string;
  description?: string;
  category: string;
  color: string;
  icon?: string;
  targetDays: number;
  currentStreak: number;
  longestStreak: number;
  isCompletedToday: boolean;
  totalCompletions: number;
}

export default function HomePage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewHabitForm, setShowNewHabitForm] = useState(false);
  const [selectedView, setSelectedView] = useState<'overview' | 'charts'>('overview');

  // Fetch habits
  useEffect(() => {
    fetchHabits();
  }, []);

  async function fetchHabits() {
    try {
      const res = await fetch('/api/habits');
      const data = await res.json();
      setHabits(data);
    } catch (error) {
      console.error('Error fetching habits:', error);
    } finally {
      setLoading(false);
    }
  }

  async function toggleCompletion(habitId: string, isCompleted: boolean) {
    try {
      if (isCompleted) {
        // Remove completion
        await fetch(`/api/habits/${habitId}/complete`, {
          method: 'DELETE',
        });
      } else {
        // Add completion
        await fetch(`/api/habits/${habitId}/complete`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ date: startOfDay(new Date()) }),
        });
      }

      // Refresh habits
      fetchHabits();
    } catch (error) {
      console.error('Error toggling completion:', error);
    }
  }

  async function createHabit(data: any) {
    try {
      await fetch('/api/habits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      setShowNewHabitForm(false);
      fetchHabits();
    } catch (error) {
      console.error('Error creating habit:', error);
    }
  }

  // Calculate overall stats
  const totalHabits = habits.length;
  const completedToday = habits.filter(h => h.isCompletedToday).length;
  const totalStreaks = habits.reduce((sum, h) => sum + h.currentStreak, 0);
  const longestStreak = Math.max(...habits.map(h => h.longestStreak), 0);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading habits...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Habit Tracker
              </h1>
              <p className="text-gray-600 mt-1">
                {format(new Date(), 'EEEE, MMMM d, yyyy')}
              </p>
            </div>

            <button
              onClick={() => setShowNewHabitForm(true)}
              className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
            >
              <Plus size={20} />
              New Habit
            </button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-4 text-white">
              <div className="flex items-center gap-2 mb-2">
                <Target size={20} />
                <span className="text-sm font-medium">Total Habits</span>
              </div>
              <div className="text-3xl font-bold">{totalHabits}</div>
            </div>

            <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-4 text-white">
              <div className="flex items-center gap-2 mb-2">
                <Check size={20} />
                <span className="text-sm font-medium">Done Today</span>
              </div>
              <div className="text-3xl font-bold">{completedToday}/{totalHabits}</div>
            </div>

            <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg p-4 text-white">
              <div className="flex items-center gap-2 mb-2">
                <Flame size={20} />
                <span className="text-sm font-medium">Active Streaks</span>
              </div>
              <div className="text-3xl font-bold">{totalStreaks}</div>
            </div>

            <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-4 text-white">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp size={20} />
                <span className="text-sm font-medium">Longest Streak</span>
              </div>
              <div className="text-3xl font-bold">{longestStreak}</div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* View Toggle */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setSelectedView('overview')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              selectedView === 'overview'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Calendar className="inline mr-2" size={18} />
            Overview
          </button>
          <button
            onClick={() => setSelectedView('charts')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              selectedView === 'charts'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <TrendingUp className="inline mr-2" size={18} />
            Progress Charts
          </button>
        </div>

        {selectedView === 'overview' ? (
          <>
            {habits.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm p-12 text-center">
                <Target size={48} className="mx-auto text-gray-400 mb-4" />
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  No habits yet
                </h2>
                <p className="text-gray-600 mb-6">
                  Start building better habits by creating your first one!
                </p>
                <button
                  onClick={() => setShowNewHabitForm(true)}
                  className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition"
                >
                  Create Your First Habit
                </button>
              </div>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {habits.map(habit => (
                  <HabitCard
                    key={habit.id}
                    habit={habit}
                    onToggle={() => toggleCompletion(habit.id, habit.isCompletedToday)}
                  />
                ))}
              </div>
            )}
          </>
        ) : (
          <ProgressChart habits={habits} />
        )}
      </main>

      {/* New Habit Modal */}
      {showNewHabitForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
            <HabitForm
              onSubmit={createHabit}
              onCancel={() => setShowNewHabitForm(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
