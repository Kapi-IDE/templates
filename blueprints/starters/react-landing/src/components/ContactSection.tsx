export function ContactSection() {
  return (
    <section className="contact-section" id="contact">
      <div className="auto-container">
        <div className="sec-title centered">
          <div className="title">Contact</div>
          <h2>Let’s craft the next chapter together.</h2>
        </div>
        <div className="row clearfix">
          <div className="form-column col-lg-8 col-md-12 col-sm-12">
            <div className="inner-column">
              <form className="contact-form">
                <div className="row clearfix">
                  <div className="col-md-6 col-sm-12 form-group">
                    <input type="text" name="name" placeholder="Your name" required />
                  </div>
                  <div className="col-md-6 col-sm-12 form-group">
                    <input type="email" name="email" placeholder="Email address" required />
                  </div>
                  <div className="col-md-12 col-sm-12 form-group">
                    <textarea name="message" placeholder="Project details" rows={5} />
                  </div>
                  <div className="col-md-12 col-sm-12 form-group">
                    <button className="theme-btn btn-style-one" type="submit">
                      <span className="btn-wrap">
                        <span className="text-one">Send message</span>
                        <span className="text-two">Send message</span>
                      </span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div className="info-column col-lg-4 col-md-12 col-sm-12">
            <div className="inner-column">
              <h4>Offices</h4>
              <ul className="contact-info">
                <li><strong>San Francisco</strong><br /> 11 Market Street</li>
                <li><strong>Berlin</strong><br /> 92 Torstraße</li>
              </ul>
              <h4>Connect</h4>
              <ul className="contact-info">
                <li><a href="mailto:hello@braine.agency">hello@braine.agency</a></li>
                <li><a href="tel:+14150000000">+1 (415) 000-0000</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
