const quotes = [
  {
    text: 'They function like an internal team. We ship faster and with more confidence.',
    author: 'Elena Torres',
    role: 'VP Product, Nimbus Analytics',
  },
  {
    text: 'From brand to build, every experience exceeded expectations.',
    author: 'Marcus Chen',
    role: 'Founder, Fieldwave',
  },
];

export function Testimonials() {
  return (
    <section className="testimonial-section" id="team">
      <div className="auto-container">
        <div className="sec-title centered">
          <div className="title">Testimonials</div>
          <h2>Trusted partners for high-growth teams.</h2>
        </div>
        <div className="row clearfix">
          {quotes.map((quote) => (
            <div className="testimonial-block col-lg-6 col-md-12 col-sm-12" key={quote.author}>
              <div className="inner-box">
                <div className="text">“{quote.text}”</div>
                <div className="author">{quote.author}</div>
                <div className="designation">{quote.role}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
