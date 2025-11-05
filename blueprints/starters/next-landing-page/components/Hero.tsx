'use client';

import { clsx } from 'clsx';

interface HeroProps {
  onPrimaryAction?: () => void;
}

export function Hero({ onPrimaryAction }: HeroProps) {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(37,99,235,0.3),_transparent_55%)]" aria-hidden />
      <div className="relative mx-auto flex max-w-6xl flex-col gap-10 px-6 pb-24 pt-32 text-center sm:px-10">
        <span className="mx-auto inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1 text-sm font-medium text-white/80">
          <span className="h-2 w-2 rounded-full bg-accent" aria-hidden />
          LaunchCanvas Starter
        </span>
        <h1 className="text-balance text-4xl font-semibold leading-tight text-white sm:text-6xl">
          Ship a polished landing page in a single afternoon.
        </h1>
        <p className="mx-auto max-w-2xl text-balance text-lg text-white/70 sm:text-xl">
          This Next.js starter gives you a production-ready marketing site with a hero section, feature highlights, testimonials, and conversion-ready call to action blocks—all wired with Tailwind CSS and responsive out of the box.
        </p>
        <div className="mx-auto flex flex-wrap items-center justify-center gap-4">
          <button
            type="button"
            onClick={onPrimaryAction}
            className={clsx(
              'inline-flex items-center justify-center rounded-full px-6 py-3 text-base font-semibold transition',
              'bg-primary text-primary-foreground hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary'
            )}
          >
            Preview the blueprint
          </button>
          <a
            href="#sections"
            className="inline-flex items-center justify-center rounded-full border border-white/15 px-6 py-3 text-base font-semibold text-white/80 transition hover:bg-white/10"
          >
            See section library
          </a>
        </div>
      </div>
    </section>
  );
}
