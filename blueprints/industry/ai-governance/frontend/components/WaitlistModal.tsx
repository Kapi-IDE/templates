'use client';

import { useEffect, useState } from 'react';

interface WaitlistModalProps {
  formAction?: string;
}

export function WaitlistModal({ formAction = 'https://example.com/waitlist' }: WaitlistModalProps) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handler = () => setOpen(true);
    window.addEventListener('openWaitlistModal', handler);
    return () => window.removeEventListener('openWaitlistModal', handler);
  }, []);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-slate-950 p-6 shadow-xl shadow-black/40">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-lg font-semibold text-white">Join the waitlist</h3>
            <p className="mt-1 text-sm text-white/70">
              Drop your email and we&apos;ll send you launch resources and updates.
            </p>
          </div>
          <button
            type="button"
            className="text-white/60 transition hover:text-white"
            onClick={() => setOpen(false)}
            aria-label="Close waitlist modal"
          >
            ×
          </button>
        </div>
        <form className="mt-6 space-y-4" action={formAction} method="post">
          <input
            type="email"
            name="email"
            required
            placeholder="you@example.com"
            className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-sm text-white placeholder:text-white/40 focus:border-primary focus:outline-none"
          />
          <button
            type="submit"
            className="w-full rounded-xl bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
          >
            Join the waitlist
          </button>
        </form>
      </div>
    </div>
  );
}
