import React, { useState } from 'react';
import PropTypes from 'prop-types';
import SearchBar from '../ui/SearchBar';
import NotificationDropdown from '../ui/NotificationDropdown';
import UserDropdown from '../ui/UserDropdown';

/**
 * Header - Top navigation bar
 */
export function Header({ onSidebarToggle, user, notifications = [] }) {
  const [searchOpen, setSearchOpen] = useState(false);

  const defaultUser = {
    name: 'Admin User',
    email: 'admin@aigovernance.com',
    avatar: '/assets/images/avatars/01.png'
  };

  const userData = user || defaultUser;

  return (
    <header className="top-header">
      <nav className="navbar navbar-expand align-items-center gap-4">
        <div className="btn-toggle" onClick={onSidebarToggle}>
          <a href="javascript:;">
            <i className="material-icons-outlined">menu</i>
          </a>
        </div>

        <SearchBar
          isOpen={searchOpen}
          onToggle={() => setSearchOpen(!searchOpen)}
        />

        <ul className="navbar-nav gap-1 nav-right-links align-items-center">
          <li className="nav-item d-lg-none mobile-search-btn">
            <a className="nav-link" href="javascript:;" onClick={() => setSearchOpen(!searchOpen)}>
              <i className="material-icons-outlined">search</i>
            </a>
          </li>

          <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle dropdown-toggle-nocaret" href="javascript:;" data-bs-toggle="dropdown">
              <img src="/assets/images/county/02.png" width="22" alt="Country" />
            </a>
            <ul className="dropdown-menu dropdown-menu-end">
              <li>
                <a className="dropdown-item d-flex align-items-center" href="javascript:;">
                  <img src="/assets/images/county/01.png" width="20" alt="USA" />
                  <span className="ms-2">USA</span>
                </a>
              </li>
              <li>
                <a className="dropdown-item d-flex align-items-center" href="javascript:;">
                  <img src="/assets/images/county/02.png" width="20" alt="UK" />
                  <span className="ms-2">UK</span>
                </a>
              </li>
            </ul>
          </li>

          <NotificationDropdown notifications={notifications} />

          <UserDropdown user={userData} />
        </ul>
      </nav>
    </header>
  );
}

Header.propTypes = {
  onSidebarToggle: PropTypes.func.isRequired,
  user: PropTypes.shape({
    name: PropTypes.string,
    email: PropTypes.string,
    avatar: PropTypes.string,
  }),
  notifications: PropTypes.array
};

export default Header;
