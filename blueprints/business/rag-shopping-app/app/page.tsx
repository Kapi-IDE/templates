'use client';

import { useState } from 'react';
import { Search, ShoppingCart, Sparkles } from 'lucide-react';
import ProductGrid from '../components/ProductGrid';
import SearchBar from '../components/SearchBar';
import ShoppingAssistant from '../components/ShoppingAssistant';
import Cart from '../components/Cart';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [cart, setCart] = useState<string[]>([]);
  const [showCart, setShowCart] = useState(false);
  const [showAssistant, setShowAssistant] = useState(false);

  const addToCart = (productId: string) => {
    setCart(prev => [...prev, productId]);
  };

  const removeFromCart = (productId: string) => {
    setCart(prev => prev.filter(id => id !== productId));
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-blue-600" />
              SmartShop
            </h1>

            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowAssistant(!showAssistant)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                AI Assistant
              </button>

              <button
                onClick={() => setShowCart(!showCart)}
                className="relative p-2 hover:bg-gray-100 rounded-lg transition"
              >
                <ShoppingCart className="w-6 h-6 text-gray-700" />
                {cart.length > 0 && (
                  <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cart.length}
                  </span>
                )}
              </button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="mt-4">
            <SearchBar onSearch={setSearchQuery} />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ProductGrid
          searchQuery={searchQuery}
          onAddToCart={addToCart}
        />
      </div>

      {/* Shopping Assistant Sidebar */}
      {showAssistant && (
        <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50 transform transition-transform">
          <ShoppingAssistant onClose={() => setShowAssistant(false)} />
        </div>
      )}

      {/* Cart Sidebar */}
      {showCart && (
        <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50">
          <Cart
            productIds={cart}
            onRemove={removeFromCart}
            onClose={() => setShowCart(false)}
          />
        </div>
      )}

      {/* Overlay */}
      {(showAssistant || showCart) && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => {
            setShowAssistant(false);
            setShowCart(false);
          }}
        />
      )}
    </main>
  );
}
