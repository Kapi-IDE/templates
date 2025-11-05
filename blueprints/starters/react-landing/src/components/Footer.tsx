export function Footer() {
  return (
    <footer className="main-footer">
      <div className="auto-container">
        <div className="widgets-section">
          <div className="row clearfix">
            <div className="footer-column col-lg-4 col-md-6 col-sm-12">
              <div className="footer-widget logo-widget">
                <div className="logo">
                  <img src="/images/logo.svg" alt="Braine" height={32} />
                </div>
                <div className="text">
                  Braine is a multidisciplinary agency crafting ambitious brand, product, and marketing experiences for digital-first companies.
                </div>
              </div>
            </div>
            <div className="footer-column col-lg-4 col-md-6 col-sm-12">
              <div className="footer-widget links-widget">
                <h4>Explore</h4>
                <ul className="list">
                  <li><a href="#services">Services</a></li>
                  <li><a href="#cases">Case studies</a></li>
                  <li><a href="#team">Team</a></li>
                  <li><a href="#blog">Blog</a></li>
                </ul>
              </div>
            </div>
            <div className="footer-column col-lg-4 col-md-12 col-sm-12">
              <div className="footer-widget newsletter-widget">
                <h4>Stay in the loop</h4>
                <div className="text">Monthly insights on product strategy and creative technology.</div>
                <form className="newsletter-form">
                  <input type="email" name="email" placeholder="Email address" required />
                  <button type="submit" className="theme-btn btn-style-one">
                    <span className="btn-wrap">
                      <span className="text-one">Subscribe</span>
                      <span className="text-two">Subscribe</span>
                    </span>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          © {new Date().getFullYear()} Braine Creative Studio. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
