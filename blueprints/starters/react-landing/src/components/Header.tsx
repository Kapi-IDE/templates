import Link from 'next/link';

const navItems = [
  { href: '#services', label: 'Services' },
  { href: '#cases', label: 'Work' },
  { href: '#team', label: 'Team' },
  { href: '#blog', label: 'Insights' },
  { href: '#contact', label: 'Contact' },
];

export function Header() {
  return (
    <header className="main-header">
      <div className="header-lower">
        <div className="auto-container">
          <div className="inner-container d-flex justify-content-between align-items-center flex-wrap">
            <div className="logo-box">
              <div className="logo">
                <Link href="/">
                  <img src="/images/logo.svg" alt="Braine" height={32} />
                </Link>
              </div>
            </div>
            <nav className="main-menu d-none d-md-block">
              <ul className="navigation clearfix">
                {navItems.map((item) => (
                  <li key={item.href}>
                    <a href={item.href}>{item.label}</a>
                  </li>
                ))}
              </ul>
            </nav>
            <a href="#contact" className="theme-btn btn-style-one">
              <span className="btn-wrap">
                <span className="text-one">Let&apos;s talk</span>
                <span className="text-two">Let&apos;s talk</span>
              </span>
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
