import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js';

const HeavyHitterPieChart = ({ total, heavyHitters, dateRange }) => {
  const chartRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      chartRef.current.destroy();
      chartRef.current = null;
    }

    const ctx = canvasRef.current.getContext('2d');

    if (!heavyHitters || heavyHitters.length === 0) return;

    const filteredHeavyHitters = heavyHitters.filter(element => element.amount > 0);

    const colors = [
      '#FFC107',
      '#73C238',
      '#0097A7',
      '#9C27B0',
      '#66D9EF',
      '#EC407A',
      '#8BC34A'
    ];

    chartRef.current = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: filteredHeavyHitters.map(element => element.name || element.category),
        datasets: [
          {
            data: filteredHeavyHitters.map(element => element.amount),
            backgroundColor: colors,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#FFFFFF',
              font: {
                size: 12
              }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const amount = context.raw || 0;
                return `${context.label}: $${amount.toLocaleString()}`;
              }
            }
          }
        },
        title: {
          display: true,
          text: 'Heavy Hitters by Category',
          color: '#FFFFFF',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
        chartRef.current = null;
      }
    };
  }, [heavyHitters, dateRange]);

  const startDate = dateRange.start_month;
  const endDate = dateRange.end_month;

  return (
    <div className="bg-gray-800">
      <div className="h-[30rem]">
        <canvas ref={canvasRef}></canvas>
      </div>
      <div className="text-center mt-4 text-white">
        <p className="text-lg font-semibold">
          Total Credit Card Spending : ${total.toLocaleString()}
        </p>
        <p className="text-sm text-gray-400">
          {startDate} - {endDate}
        </p>
      </div>
    </div>
  );
};

export default HeavyHitterPieChart;