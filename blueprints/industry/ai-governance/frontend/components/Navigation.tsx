'use client';

const navLinks = [
  { href: '#sections', label: 'Sections' },
  { href: '#testimonials', label: 'Proof' },
  { href: '#contact', label: 'Contact' },
];

export function Navigation() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/70 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 sm:px-10">
        <span className="text-lg font-semibold text-white">LaunchCanvas</span>
        <nav className="hidden items-center gap-6 text-sm text-white/70 sm:flex">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href} className="hover:text-white">
              {link.label}
            </a>
          ))}
        </nav>
        <button
          type="button"
          onClick={() => window.dispatchEvent(new Event('openWaitlistModal'))}
          className="hidden rounded-full border border-white/15 px-4 py-2 text-sm font-semibold text-white transition hover:bg-white/10 sm:inline-flex"
        >
          Join waitlist
        </button>
      </div>
    </header>
  );
}
