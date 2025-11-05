const features = [
  {
    title: 'Focus on copy, not plumbing',
    description:
      'Pre-built hero, feature, metrics, and testimonial sections that map to common SaaS story arcs. Swap the content and launch.',
  },
  {
    title: 'Responsive out of the box',
    description:
      'Tailwind utility classes keep typography and spacing consistent from mobile to desktop without extra tweaking.',
  },
  {
    title: 'SEO ready metadata',
    description:
      'Opinionated metadata and structured data give search engines everything they need from day one.',
  },
  {
    title: 'Dark UI aesthetic',
    description:
      'Clean slate palette with accent colors that work across hero gradients, cards, and buttons.',
  },
];

export function FeatureGrid() {
  return (
    <section id="sections" className="border-t border-white/10 bg-white/5/5">
      <div className="mx-auto max-w-5xl px-6 py-20 sm:px-10">
        <div className="mb-12 max-w-2xl">
          <h2 className="text-3xl font-semibold text-white sm:text-4xl">
            Everything marketing teams expect, ready to customise.
          </h2>
          <p className="mt-4 text-white/70">
            Each section lives in its own React component so you can reorder, duplicate, or remove them without touching layout glue.
          </p>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          {features.map((feature) => (
            <article
              key={feature.title}
              className="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-lg shadow-black/20"
            >
              <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
              <p className="mt-3 text-sm text-white/70">{feature.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
