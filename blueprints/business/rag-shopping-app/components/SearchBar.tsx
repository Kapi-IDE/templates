'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const EXAMPLE_QUERIES = [
  "shoes for marathon training",
  "eco-friendly workout gear",
  "gear for winter hiking",
  "gadgets for outdoor camping",
];

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="relative">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe what you're looking for... (e.g., 'shoes for marathon training')"
          className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
        />
      </form>

      {/* Example Queries */}
      <div className="mt-2 flex flex-wrap gap-2">
        <span className="text-sm text-gray-600">Try:</span>
        {EXAMPLE_QUERIES.map((example, idx) => (
          <button
            key={idx}
            onClick={() => {
              setQuery(example);
              onSearch(example);
            }}
            className="text-sm text-blue-600 hover:underline"
          >
            "{example}"
          </button>
        ))}
      </div>
    </div>
  );
}
