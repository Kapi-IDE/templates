export function Footer() {
  return (
    <footer id="contact" className="border-t border-white/10 bg-slate-950/80">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-12 text-sm text-white/60 sm:flex-row sm:items-center sm:justify-between sm:px-10">
        <p>© {new Date().getFullYear()} LaunchCanvas. Built with Next.js and Tailwind CSS.</p>
        <div className="flex gap-4">
          <a href="mailto:hello@example.com" className="hover:text-white">
            hello@example.com
          </a>
          <a href="https://github.com" className="hover:text-white" target="_blank" rel="noreferrer">
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}
