import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

/**
 * DashboardLayout - Main dashboard layout component
 * Provides the complete dashboard structure with sidebar, header, and content area
 */
export function DashboardLayout({
  children,
  theme = 'blue-theme',
  sidebarCollapsed = false,
  onSidebarToggle,
  user,
  notifications = [],
  menuItems = []
}) {
  const [collapsed, setCollapsed] = useState(sidebarCollapsed);

  const handleSidebarToggle = () => {
    const newState = !collapsed;
    setCollapsed(newState);
    if (onSidebarToggle) {
      onSidebarToggle(newState);
    }
  };

  return (
    <div className={`wrapper ${theme}`} data-bs-theme={theme}>
      {/* Sidebar */}
      <Sidebar
        collapsed={collapsed}
        onToggle={handleSidebarToggle}
        menuItems={menuItems}
      />

      {/* Main Content */}
      <main className={`main-wrapper ${collapsed ? 'sidebar-collapsed' : ''}`}>
        {/* Header */}
        <Header
          onSidebarToggle={handleSidebarToggle}
          user={user}
          notifications={notifications}
        />

        {/* Page Content */}
        <div className="main-content">
          <div className="page-breadcrumb d-none d-sm-flex align-items-center mb-3">
            <div className="breadcrumb-title pe-3">Dashboard</div>
            <div className="ps-3">
              <nav aria-label="breadcrumb">
                <ol className="breadcrumb mb-0 p-0">
                  <li className="breadcrumb-item">
                    <a href="/">
                      <i className="material-icons-outlined">home</i>
                    </a>
                  </li>
                  <li className="breadcrumb-item active" aria-current="page">
                    Analytics
                  </li>
                </ol>
              </nav>
            </div>
          </div>

          {children}
        </div>

        {/* Footer */}
        <Footer />
      </main>

      {/* Overlay for mobile */}
      {!collapsed && (
        <div
          className="sidebar-overlay d-lg-none"
          onClick={handleSidebarToggle}
        />
      )}
    </div>
  );
}

DashboardLayout.propTypes = {
  children: PropTypes.node.isRequired,
  theme: PropTypes.oneOf(['blue-theme', 'dark-theme', 'light-theme', 'semi-dark', 'bordered-theme']),
  sidebarCollapsed: PropTypes.bool,
  onSidebarToggle: PropTypes.func,
  user: PropTypes.shape({
    name: PropTypes.string,
    email: PropTypes.string,
    avatar: PropTypes.string,
  }),
  notifications: PropTypes.array,
  menuItems: PropTypes.array,
};

export default DashboardLayout;
