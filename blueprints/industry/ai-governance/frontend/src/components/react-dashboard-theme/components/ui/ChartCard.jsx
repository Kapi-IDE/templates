import React from 'react';
import PropTypes from 'prop-types';
import { Line, Bar, Doughnut, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

/**
 * ChartCard - Card with chart visualization
 */
export function ChartCard({
  title,
  subtitle,
  chartType = 'line',
  chartData,
  height = 300,
  options: customOptions
}) {
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: false,
      },
    },
  };

  const options = { ...defaultOptions, ...customOptions };

  const renderChart = () => {
    switch (chartType) {
      case 'line':
        return <Line data={chartData} options={options} />;
      case 'bar':
        return <Bar data={chartData} options={options} />;
      case 'doughnut':
        return <Doughnut data={chartData} options={options} />;
      case 'pie':
        return <Pie data={chartData} options={options} />;
      default:
        return <Line data={chartData} options={options} />;
    }
  };

  return (
    <div className="card rounded-4">
      <div className="card-header border-0 bg-transparent">
        <div className="d-flex align-items-center justify-content-between">
          <div>
            <h5 className="mb-0">{title}</h5>
            {subtitle && <p className="mb-0 text-muted">{subtitle}</p>}
          </div>
          <div className="dropdown">
            <a href="javascript:;" className="dropdown-toggle-nocaret options dropdown-toggle" data-bs-toggle="dropdown">
              <i className="material-icons-outlined">more_vert</i>
            </a>
            <ul className="dropdown-menu">
              <li><a className="dropdown-item" href="javascript:;">Download Report</a></li>
              <li><a className="dropdown-item" href="javascript:;">Export Data</a></li>
              <li><a className="dropdown-item" href="javascript:;">Refresh</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div className="card-body">
        <div style={{ height: `${height}px` }}>
          {renderChart()}
        </div>
      </div>
    </div>
  );
}

ChartCard.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string,
  chartType: PropTypes.oneOf(['line', 'bar', 'doughnut', 'pie']),
  chartData: PropTypes.object.isRequired,
  height: PropTypes.number,
  options: PropTypes.object
};

export default ChartCard;
