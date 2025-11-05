'use client';

import { useState } from 'react';
import { X } from 'lucide-react';

const CATEGORIES = [
  { value: 'health', label: '💪 Health', color: '#10B981' },
  { value: 'work', label: '💼 Work', color: '#3B82F6' },
  { value: 'learning', label: '📚 Learning', color: '#8B5CF6' },
  { value: 'personal', label: '🌟 Personal', color: '#F59E0B' },
  { value: 'general', label: '📌 General', color: '#6B7280' },
];

const COMMON_HABITS = [
  { name: 'Exercise', icon: '🏃', category: 'health' },
  { name: 'Read', icon: '📖', category: 'learning' },
  { name: 'Meditate', icon: '🧘', category: 'health' },
  { name: 'Code Practice', icon: '💻', category: 'work' },
  { name: 'Drink Water', icon: '💧', category: 'health' },
  { name: 'Journal', icon: '📝', category: 'personal' },
];

interface HabitFormProps {
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

export default function HabitForm({ onSubmit, onCancel }: HabitFormProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('general');
  const [icon, setIcon] = useState('');
  const [targetDays, setTargetDays] = useState(7);

  const selectedCategory = CATEGORIES.find(c => c.value === category);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    onSubmit({
      name,
      description: description || undefined,
      category,
      color: selectedCategory?.color || '#6B7280',
      icon: icon || undefined,
      targetDays,
      frequency: 'daily',
    });
  }

  function selectTemplate(template: typeof COMMON_HABITS[0]) {
    setName(template.name);
    setIcon(template.icon);
    setCategory(template.category);
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Create New Habit</h2>
        <button
          onClick={onCancel}
          className="text-gray-400 hover:text-gray-600 transition"
        >
          <X size={24} />
        </button>
      </div>

      {/* Quick Templates */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Quick Start (Optional)
        </label>
        <div className="grid grid-cols-3 gap-2">
          {COMMON_HABITS.map(template => (
            <button
              key={template.name}
              type="button"
              onClick={() => selectTemplate(template)}
              className="p-2 text-center bg-gray-50 hover:bg-gray-100 rounded-lg transition text-sm"
            >
              <div className="text-2xl mb-1">{template.icon}</div>
              <div className="text-xs text-gray-700">{template.name}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Habit Name *
          </label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            required
            maxLength={100}
            placeholder="e.g., Morning run"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>

        {/* Icon (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Icon (Emoji)
          </label>
          <input
            type="text"
            value={icon}
            onChange={e => setIcon(e.target.value)}
            maxLength={2}
            placeholder="🏃"
            className="w-20 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-center text-2xl"
          />
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <div className="grid grid-cols-2 gap-2">
            {CATEGORIES.map(cat => (
              <button
                key={cat.value}
                type="button"
                onClick={() => setCategory(cat.value)}
                className={`p-3 rounded-lg border-2 transition ${
                  category === cat.value
                    ? 'border-indigo-500 bg-indigo-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium text-sm">{cat.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description (Optional)
          </label>
          <textarea
            value={description}
            onChange={e => setDescription(e.target.value)}
            rows={2}
            placeholder="Why is this habit important?"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>

        {/* Target Days */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Weekly Goal: {targetDays} {targetDays === 1 ? 'day' : 'days'}
          </label>
          <input
            type="range"
            min="1"
            max="7"
            value={targetDays}
            onChange={e => setTargetDays(Number(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>1 day/week</span>
            <span>7 days/week</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-3 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={!name.trim()}
            className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
          >
            Create Habit
          </button>
        </div>
      </form>
    </div>
  );
}
