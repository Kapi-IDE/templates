import React from 'react';
import PropTypes from 'prop-types';
import { NavLink } from 'react-router-dom';

/**
 * Sidebar - Vertical navigation sidebar
 */
export function Sidebar({ collapsed, onToggle, menuItems = [] }) {
  const defaultMenuItems = [
    {
      title: 'Dashboard',
      icon: 'dashboard',
      path: '/',
      badge: { text: '5', variant: 'danger' }
    },
    {
      title: 'AI Models',
      icon: 'model_training',
      submenu: [
        { title: 'All Models', path: '/models', badge: { text: 'New', variant: 'success' } },
        { title: 'Register Model', path: '/models/register' },
        { title: 'Model Performance', path: '/models/performance' }
      ]
    },
    {
      title: 'Governance',
      icon: 'verified_user',
      submenu: [
        { title: 'Bias Detection', path: '/governance/bias' },
        { title: 'Risk Assessment', path: '/governance/risk' },
        { title: 'Compliance', path: '/governance/compliance' },
        { title: 'Audit Trail', path: '/governance/audit' }
      ]
    },
    {
      title: 'Analytics',
      icon: 'analytics',
      submenu: [
        { title: 'Overview', path: '/analytics' },
        { title: 'Reports', path: '/analytics/reports' },
        { title: 'Metrics', path: '/analytics/metrics' }
      ]
    },
    {
      title: 'Settings',
      icon: 'settings',
      path: '/settings'
    }
  ];

  const items = menuItems.length > 0 ? menuItems : defaultMenuItems;

  return (
    <aside className={`sidebar-wrapper ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="logo-icon">
          <img src="/assets/images/logo-icon.png" className="logo-img" alt="Logo" />
        </div>
        <div className="logo-name flex-grow-1">
          <h5 className="mb-0">AI Governance</h5>
        </div>
        <div className="sidebar-close" onClick={onToggle}>
          <span className="material-icons-outlined">close</span>
        </div>
      </div>

      <div className="sidebar-nav" data-simplebar>
        <ul className="metismenu" id="sidenav">
          {items.map((item, index) => (
            <MenuItem key={index} item={item} collapsed={collapsed} />
          ))}
        </ul>
      </div>
    </aside>
  );
}

function MenuItem({ item, collapsed }) {
  const [isOpen, setIsOpen] = React.useState(false);

  if (item.submenu) {
    return (
      <li>
        <a
          href="javascript:;"
          className="has-arrow"
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className="parent-icon">
            <i className="material-icons-outlined">{item.icon}</i>
          </div>
          <div className="menu-title">{item.title}</div>
        </a>
        <ul className={isOpen ? 'mm-show' : 'mm-collapse'}>
          {item.submenu.map((subItem, subIndex) => (
            <li key={subIndex}>
              <NavLink to={subItem.path}>
                <i className="material-icons-outlined">arrow_right</i>
                {subItem.title}
                {subItem.badge && (
                  <span className={`badge bg-${subItem.badge.variant} ms-auto`}>
                    {subItem.badge.text}
                  </span>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </li>
    );
  }

  return (
    <li>
      <NavLink to={item.path}>
        <div className="parent-icon">
          <i className="material-icons-outlined">{item.icon}</i>
        </div>
        <div className="menu-title">{item.title}</div>
        {item.badge && (
          <span className={`badge bg-${item.badge.variant} ms-auto`}>
            {item.badge.text}
          </span>
        )}
      </NavLink>
    </li>
  );
}

Sidebar.propTypes = {
  collapsed: PropTypes.bool,
  onToggle: PropTypes.func.isRequired,
  menuItems: PropTypes.array
};

export default Sidebar;
