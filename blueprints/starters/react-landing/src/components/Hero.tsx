'use client';

export function Hero() {
  return (
    <section className="banner-section" id="top">
      <div className="auto-container">
        <div className="row clearfix">
          <div className="content-column col-lg-6 col-md-12 col-sm-12">
            <div className="inner-column" data-wow-delay="0ms" data-wow-duration="1500ms">
              <div className="title">Digital agency</div>
              <h1>We build bold brands for digital-first companies.</h1>
              <div className="text">
                A full-stack creative team that turns complex products into delightful customer experiences. Strategy, design, and engineering working as one.
              </div>
              <div className="btn-box">
                <a href="#services" className="theme-btn btn-style-one">
                  <span className="btn-wrap">
                    <span className="text-one">Explore services</span>
                    <span className="text-two">Explore services</span>
                  </span>
                </a>
                <a href="#cases" className="theme-btn btn-style-two">
                  <span className="btn-wrap">
                    <span className="text-one">View our work</span>
                    <span className="text-two">View our work</span>
                  </span>
                </a>
              </div>
            </div>
          </div>
          <div className="image-column col-lg-6 col-md-12 col-sm-12">
            <div className="inner-column" data-wow-delay="300ms" data-wow-duration="1500ms">
              <img src="/images/resource/hero.png" alt="Hero" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
