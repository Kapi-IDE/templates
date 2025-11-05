import React from 'react';

const HealthCheck = ({ health }) => {
  if (!health) {
    return (
      <div className="flex items-center space-x-2">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
        <span className="text-sm">Checking...</span>
      </div>
    );
  }

  const isHealthy = health.status === 'healthy';

  return (
    <div className="flex items-center space-x-2">
      <div className={`w-2 h-2 rounded-full ${
        isHealthy ? 'bg-green-400' : 'bg-red-400'
      }`}></div>
      <span className="text-sm">
        {isHealthy ? 'System Healthy' : 'System Issues'}
      </span>
    </div>
  );
};

export default HealthCheck;