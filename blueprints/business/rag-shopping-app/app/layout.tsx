import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SmartShop - RAG-Powered Shopping',
  description: 'AI-powered e-commerce with semantic product search',
};

export default function RootLayout({
  children,
}: {
  children: React.Node;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
