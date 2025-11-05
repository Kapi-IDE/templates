import type { Metadata } from 'next';
import './styles/globals.css';

export const metadata: Metadata = {
  title: 'LaunchCanvas – Ship Landing Pages Fast',
  description: 'A polished Next.js landing page starter with hero, features, testimonials, and CTA sections ready for your product launch.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="min-h-screen bg-slate-950 text-white antialiased">
        {children}
      </body>
    </html>
  );
}
