/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./OnyxChatClone.tsx",
    "./RAGChatUI.tsx"
  ],
  theme: {
    extend: {
      colors: {
        'onyx': {
          'dark': '#101621',
          'light': '#1e2a38',
          'border': '#1f2c3a',
          'sidebar': '#0a0f1a',
        }
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  plugins: [],
}
