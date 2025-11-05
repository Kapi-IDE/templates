'use client';

import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';

const cases = [
  {
    image: '/images/gallery/case-1.jpg',
    title: 'Nimbus Analytics',
    description: 'Product strategy, UX, and full-stack build for an AI operations platform.',
  },
  {
    image: '/images/gallery/case-2.jpg',
    title: 'Fieldwave',
    description: 'Brand refresh and marketing site that doubled demo pipeline in 60 days.',
  },
  {
    image: '/images/gallery/case-3.jpg',
    title: 'Atlas Pay',
    description: 'Design system and mobile apps for a global fintech expansion.',
  },
];

export function CaseStudyCarousel() {
  return (
    <section className="portfolio-section" id="cases">
      <div className="auto-container">
        <div className="sec-title">
          <div className="title">Case studies</div>
          <h2>Proof we can take you from idea to launch.</h2>
        </div>
      </div>
      <Swiper slidesPerView={1.1} spaceBetween={20} breakpoints={{ 992: { slidesPerView: 2.2 } }}>
        {cases.map((item) => (
          <SwiperSlide key={item.title}>
            <article className="case-block">
              <div className="image">
                <img src={item.image} alt={item.title} />
              </div>
              <div className="lower-content">
                <h4>{item.title}</h4>
                <p>{item.description}</p>
              </div>
            </article>
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
}
