const testimonials = [
  {
    quote:
      'We swapped our custom marketing site for this starter and shipped a redesign in two days. The sections read like a creative brief.',
    author: 'Mira Patel',
    role: 'Head of Product Marketing, Foundry Labs',
  },
  {
    quote:
      'The layout feels premium without heavy design work. Clients love how quickly we can align on copy and ship updates.',
    author: 'Evan Brooks',
    role: 'Founder, Launchsmith Studio',
  },
];

export function Testimonials() {
  return (
    <section className="border-t border-white/10 bg-slate-950/60">
      <div className="mx-auto flex max-w-5xl flex-col gap-10 px-6 py-20 sm:px-10 md:flex-row">
        <div className="max-w-sm">
          <h2 className="text-3xl font-semibold text-white sm:text-4xl">
            Loved by teams who iterate fast.
          </h2>
          <p className="mt-4 text-sm text-white/70">
            Ideal for early-stage launches, agency retainers, and product refresh cycles where momentum matters.
          </p>
        </div>
        <div className="flex-1 space-y-6">
          {testimonials.map((testimonial) => (
            <figure key={testimonial.author} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <blockquote className="text-lg text-white/90">“{testimonial.quote}”</blockquote>
              <figcaption className="mt-4 text-sm text-white/70">
                <span className="font-medium text-white">{testimonial.author}</span> · {testimonial.role}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
