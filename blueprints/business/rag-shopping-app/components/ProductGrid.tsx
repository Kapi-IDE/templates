'use client';

import { useState, useEffect } from 'react';
import { ShoppingCart, Sparkles } from 'lucide-react';
import products from '../data/products.json';

interface ProductGridProps {
  searchQuery: string;
  onAddToCart: (productId: string) => void;
}

interface ProductWithScore {
  id: string;
  name: string;
  category: string;
  price: number;
  description: string;
  tags: string[];
  image: string;
  similarity?: number;
  reasoning?: string;
}

export default function ProductGrid({ searchQuery, onAddToCart }: ProductGridProps) {
  const [displayProducts, setDisplayProducts] = useState<ProductWithScore[]>(products);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setDisplayProducts(products);
      return;
    }

    // Semantic search via API
    const search = async () => {
      setLoading(true);
      try {
        const res = await fetch('/api/products/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: searchQuery }),
        });

        const data = await res.json();
        setDisplayProducts(data.products || []);
      } catch (error) {
        console.error('Search failed:', error);
        setDisplayProducts(products);
      } finally {
        setLoading(false);
      }
    };

    search();
  }, [searchQuery]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Searching products...</p>
      </div>
    );
  }

  return (
    <div>
      {searchQuery && (
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-2">
            <Sparkles className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-blue-900">
                AI-Powered Search Results
              </p>
              <p className="text-sm text-blue-700 mt-1">
                Found {displayProducts.length} products matching "{searchQuery}"
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {displayProducts.map((product) => (
          <div
            key={product.id}
            className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition overflow-hidden"
          >
            {/* Product Image Placeholder */}
            <div className="h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
              <div className="text-6xl">{getCategoryEmoji(product.category)}</div>
            </div>

            {/* Product Info */}
            <div className="p-4">
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="font-semibold text-gray-900 text-sm line-clamp-2">
                  {product.name}
                </h3>
                <span className="text-lg font-bold text-blue-600 whitespace-nowrap">
                  ${product.price}
                </span>
              </div>

              <p className="text-xs text-gray-600 mb-3 line-clamp-2">
                {product.description}
              </p>

              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  {product.category}
                </span>

                <button
                  onClick={() => onAddToCart(product.id)}
                  className="flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white text-xs rounded-lg hover:bg-blue-700 transition"
                >
                  <ShoppingCart className="w-3 h-3" />
                  Add
                </button>
              </div>

              {/* Show similarity score if from semantic search */}
              {product.similarity !== undefined && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-3 h-3 text-blue-600" />
                    <span className="text-xs text-blue-600">
                      {Math.round(product.similarity * 100)}% match
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {displayProducts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">No products found for "{searchQuery}"</p>
          <p className="text-sm text-gray-500 mt-2">Try a different search query</p>
        </div>
      )}
    </div>
  );
}

function getCategoryEmoji(category: string): string {
  const emojiMap: Record<string, string> = {
    'Footwear': '👟',
    'Electronics': '🎧',
    'Fitness': '🏋️',
    'Apparel': '👕',
    'Accessories': '🎒',
    'Outdoor Gear': '⛺',
    'Home': '🏠',
  };
  return emojiMap[category] || '📦';
}
