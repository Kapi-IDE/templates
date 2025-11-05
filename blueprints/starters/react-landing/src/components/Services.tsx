const services = [
  {
    icon: '/images/icons/service-1.svg',
    title: 'Brand Strategy',
    description: 'Positioning, messaging, and visual identity systems for modern SaaS teams.',
  },
  {
    icon: '/images/icons/service-2.svg',
    title: 'Product Design',
    description: 'Cross-platform design systems, prototyping, and UX research to launch faster.',
  },
  {
    icon: '/images/icons/service-3.svg',
    title: 'Engineering',
    description: 'Full-stack product development across web, mobile, and backend infrastructure.',
  },
];

export function Services() {
  return (
    <section className="services-section" id="services">
      <div className="auto-container">
        <div className="sec-title centered">
          <div className="title">Capabilities</div>
          <h2>Integrated teams that ship value in weeks, not months.</h2>
        </div>
        <div className="row clearfix">
          {services.map((service) => (
            <div className="service-block col-lg-4 col-md-6 col-sm-12" key={service.title}>
              <div className="inner-box wow fadeInUp" data-wow-delay="0ms" data-wow-duration="1500ms">
                <div className="icon-box">
                  <img src={service.icon} alt="" />
                </div>
                <h4>{service.title}</h4>
                <div className="text">{service.description}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
