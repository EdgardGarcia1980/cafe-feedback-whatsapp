import React from 'react';

const StatsCard = ({ title, value, subtitle, icon, color = 'blue' }) => {
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
    purple: 'bg-purple-500',
    yellow: 'bg-yellow-500'
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-gray-500 text-sm font-medium uppercase mb-1">
            {title}
          </p>
          <p className="text-3xl font-bold text-gray-800">
            {value}
          </p>
          {subtitle && (
            <p className="text-gray-600 text-sm mt-1">
              {subtitle}
            </p>
          )}
        </div>
        {icon && (
          <div className={`${colorClasses[color]} p-3 rounded-full`}>
            <span className="text-white text-2xl">{icon}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatsCard;
