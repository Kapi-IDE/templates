import { Header } from '../components/Header';
import { Hero } from '../components/Hero';
import { Services } from '../components/Services';
import { CaseStudyCarousel } from '../components/CaseStudyCarousel';
import { Testimonials } from '../components/Testimonials';
import { ContactSection } from '../components/ContactSection';
import { Footer } from '../components/Footer';

export default function Page() {
  return (
    <div className="page-wrapper">
      <div className="cursor" />
      <div className="cursor-follower" />
      <Header />
      <Hero />
      <Services />
      <CaseStudyCarousel />
      <Testimonials />
      <ContactSection />
      <Footer />
    </div>
  );
}
