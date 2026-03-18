import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const SentimentChart = ({ data }) => {
  const COLORS = {
    positivo: '#10B981',  // green
    negativo: '#EF4444',  // red
    neutro: '#6B7280'     // gray
  };

  const chartData = [
    { name: 'Positivo', value: data?.counts?.positivo || 0, percentage: data?.percentages?.positivo || 0 },
    { name: 'Negativo', value: data?.counts?.negativo || 0, percentage: data?.percentages?.negativo || 0 },
    { name: 'Neutro', value: data?.counts?.neutro || 0, percentage: data?.percentages?.neutro || 0 }
  ].filter(item => item.value > 0);

  if (chartData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Distribución de Sentimientos</h2>
        <div className="flex items-center justify-center h-64 text-gray-400">
          No hay datos disponibles
        </div>
      </div>
    );
  }

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        className="font-bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Distribución de Sentimientos</h2>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={CustomLabel}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name.toLowerCase()]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name, props) => [
              `${value} mensajes (${props.payload.percentage}%)`,
              props.payload.name
            ]}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
      <div className="mt-4 grid grid-cols-3 gap-4 text-center">
        {chartData.map((item) => (
          <div key={item.name}>
            <div
              className="w-4 h-4 rounded-full mx-auto mb-1"
              style={{ backgroundColor: COLORS[item.name.toLowerCase()] }}
            ></div>
            <p className="text-sm font-semibold">{item.name}</p>
            <p className="text-xs text-gray-600">{item.value} ({item.percentage}%)</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SentimentChart;
