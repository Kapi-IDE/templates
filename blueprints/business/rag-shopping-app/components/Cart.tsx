'use client';

import { X, Trash2 } from 'lucide-react';
import products from '../data/products.json';

interface CartProps {
  productIds: string[];
  onRemove: (productId: string) => void;
  onClose: () => void;
}

export default function Cart({ productIds, onRemove, onClose }: CartProps) {
  const cartItems = productIds.map(id => products.find(p => p.id === id)!).filter(Boolean);
  const total = cartItems.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <h2 className="font-semibold text-lg">Shopping Cart</h2>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded transition"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Cart Items */}
      <div className="flex-1 overflow-y-auto p-4">
        {cartItems.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Your cart is empty</p>
            <p className="text-sm text-gray-500 mt-2">Add some products to get started!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {cartItems.map((item, idx) => (
              <div
                key={`${item.id}-${idx}`}
                className="flex gap-3 p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <h3 className="font-medium text-sm">{item.name}</h3>
                  <p className="text-gray-600 text-xs mt-1">{item.category}</p>
                  <p className="text-blue-600 font-semibold mt-2">${item.price}</p>
                </div>
                <button
                  onClick={() => onRemove(productIds[idx])}
                  className="p-2 hover:bg-red-50 text-red-600 rounded transition"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      {cartItems.length > 0 && (
        <div className="border-t p-4 space-y-4">
          <div className="flex items-center justify-between text-lg font-semibold">
            <span>Total:</span>
            <span className="text-blue-600">${total.toFixed(2)}</span>
          </div>
          <button className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium">
            Checkout ({cartItems.length} {cartItems.length === 1 ? 'item' : 'items'})
          </button>
        </div>
      )}
    </div>
  );
}
