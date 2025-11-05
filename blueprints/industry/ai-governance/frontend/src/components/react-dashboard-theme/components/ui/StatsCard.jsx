import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

/**
 * StatsCard - Statistics display card
 */
export function StatsCard({
  title,
  value,
  icon,
  trend = 'neutral',
  percentage,
  color = 'primary',
  subtitle,
  onClick
}) {
  const trendIcon = trend === 'up' ? 'arrow_drop_up' :
                    trend === 'down' ? 'arrow_drop_down' : 'remove';

  const trendColor = trend === 'up' ? 'success' :
                     trend === 'down' ? 'danger' : 'secondary';

  return (
    <div className="col">
      <div
        className={classNames('card rounded-4', { 'cursor-pointer': onClick })}
        onClick={onClick}
      >
        <div className="card-body">
          <div className="d-flex align-items-center gap-3 mb-2">
            <div className={`widget-icon bg-${color} text-white rounded-circle`}>
              <i className="material-icons-outlined">{icon}</i>
            </div>
            <div className="flex-grow-1">
              <p className="mb-0 text-secondary">{title}</p>
              <h4 className="my-1">{value}</h4>
              {subtitle && <p className="mb-0 text-muted small">{subtitle}</p>}
            </div>
          </div>
          {percentage !== undefined && (
            <div className="d-flex align-items-center gap-1">
              <span className={`text-${trendColor} me-1`}>
                <i className="material-icons-outlined fs-6">{trendIcon}</i>
              </span>
              <p className="mb-0">{percentage}%</p>
              <p className="mb-0 ms-auto text-secondary">{trend === 'up' ? 'vs last month' : ''}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

StatsCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  icon: PropTypes.string.isRequired,
  trend: PropTypes.oneOf(['up', 'down', 'neutral']),
  percentage: PropTypes.number,
  color: PropTypes.oneOf(['primary', 'secondary', 'success', 'danger', 'warning', 'info']),
  subtitle: PropTypes.string,
  onClick: PropTypes.func
};

export default StatsCard;
