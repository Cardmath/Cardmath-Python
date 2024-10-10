import React from 'react';
import { Chart } from 'primereact/chart';


const HeavyHitterPieChart = ({ heavyHitters, type }) => {

  const chartData = {
    labels: heavyHitters.map(element => element.category),
    datasets: [
      {
        data: heavyHitters.map(element => element.percent),
      }
    ]
  };
  const colors = [
    '#FFC107',
    '#73C238',
    '#0097A7',
    '#9C27B0',
    '#66D9EF',
    '#EC407A',
    '#8BC34A'
  ];

  // Options for the pie chart
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      }
    },
    datasets: {
      pie: {
        backgroundColor: colors
      }
    }
  };

  return (
    
    <div>
      {heavyHitters && heavyHitters.length && <Chart type="pie" data={chartData} options={chartOptions} />}
    </div>
  );
};

export default HeavyHitterPieChart;
