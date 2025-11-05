interface CallToActionProps {
  onJoinWaitlist?: () => void;
}

export function CallToAction({ onJoinWaitlist }: CallToActionProps) {
  return (
    <section className="border-t border-white/10 bg-gradient-to-br from-primary/20 via-slate-950 to-slate-950">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-16 text-center sm:px-10">
        <h2 className="text-balance text-3xl font-semibold text-white sm:text-4xl">
          Ready to launch? Export the blueprint, plug in your product, and share it today.
        </h2>
        <p className="mx-auto max-w-2xl text-white/70">
          Clone the repository, update the copy blocks, and deploy to Vercel or Netlify in minutes. The starter is licensed under MIT so you can ship without friction.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4">
          <a
            className="inline-flex items-center justify-center rounded-full bg-white px-6 py-3 text-base font-semibold text-slate-900 shadow-lg shadow-primary/40 transition hover:-translate-y-[1px]"
            href="https://vercel.com/new"
            target="_blank"
            rel="noreferrer"
          >
            Deploy to Vercel
          </a>
          <button
            type="button"
            onClick={onJoinWaitlist}
            className="inline-flex items-center justify-center rounded-full border border-white/15 px-6 py-3 text-base font-semibold text-white transition hover:bg-white/10"
          >
            Duplicate template
          </button>
        </div>
      </div>
    </section>
  );
}
