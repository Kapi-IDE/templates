import type { Metadata } from 'next';
import { Hero } from '../components/Hero';
import { FeatureGrid } from '../components/FeatureGrid';
import { StatsPanel } from '../components/StatsPanel';
import { Testimonials } from '../components/Testimonials';
import { CallToAction } from '../components/CallToAction';
import { Navigation } from '../components/Navigation';
import { WaitlistModal } from '../components/WaitlistModal';
import { Footer } from '../components/Footer';

export const metadata: Metadata = {
  title: 'LaunchCanvas – Next.js Landing Page Starter',
  description:
    'A polished marketing site for SaaS launches. Includes hero, feature, testimonial, and CTA sections wired with Next.js App Router and Tailwind CSS.',
  openGraph: {
    title: 'LaunchCanvas – Next.js Landing Page Starter',
    description:
      'A polished marketing site for SaaS launches. Includes hero, feature, testimonial, and CTA sections wired with Next.js App Router and Tailwind CSS.',
    url: 'https://example.com',
    type: 'website',
    images: [
      {
        url: 'https://via.placeholder.com/1200x630.png?text=LaunchCanvas',
        width: 1200,
        height: 630,
        alt: 'LaunchCanvas preview',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'LaunchCanvas – Next.js Landing Page Starter',
    description:
      'A polished marketing site for SaaS launches. Includes hero, feature, testimonial, and CTA sections wired with Next.js App Router and Tailwind CSS.',
    images: ['https://via.placeholder.com/1200x630.png?text=LaunchCanvas'],
  },
};

export default function Page() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'LaunchCanvas Landing Page Starter',
    description:
      'A production-ready marketing site template for founders and agencies building with Next.js and Tailwind CSS.',
    url: 'https://example.com',
    creator: {
      '@type': 'Organization',
      name: 'LaunchCanvas',
    },
  };

  const handlePrimaryAction = () => {
    window.dispatchEvent(new Event('openWaitlistModal'));
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <Navigation />
      <main className="flex flex-col">
        <Hero onPrimaryAction={handlePrimaryAction} />
        <StatsPanel />
        <FeatureGrid />
        <Testimonials />
        <CallToAction onJoinWaitlist={handlePrimaryAction} />
      </main>
      <Footer />
      <WaitlistModal formAction="https://example.com/api/waitlist" />
    </>
  );
}
