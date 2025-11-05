import React from 'react';
import PropTypes from 'prop-types';

const Card = ({ title, subtitle, children, actions }) => (
  <section className="card">
    <header className="card__header">
      <div>
        <h2>{title}</h2>
        {subtitle && <p className="card__subtitle">{subtitle}</p>}
      </div>
      {actions && <div className="card__actions">{actions}</div>}
    </header>
    <div className="card__body">{children}</div>
  </section>
);

Card.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string,
  children: PropTypes.node.isRequired,
  actions: PropTypes.node,
};

export default Card;
