import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js';

const HeavyHitterPieChart = ({ heavyHitters, type }) => {
  const chartRef = useRef(null); // Store chart instance
  const canvasRef = useRef(null); // Store canvas DOM element

  useEffect(() => {
    // Destroy existing chart if it exists to avoid the "canvas already in use" error
    if (chartRef.current) {
      chartRef.current.destroy();
      chartRef.current = null; // Set to null to fully clear
    }

    const ctx = canvasRef.current.getContext('2d');

    // If no data is available, don't attempt to create the chart
    if (!heavyHitters || heavyHitters.length === 0) {
      return;
    }

    const colors = [
      '#FFC107',
      '#73C238',
      '#0097A7',
      '#9C27B0',
      '#66D9EF',
      '#EC407A',
      '#8BC34A'
    ];

    // Create new chart instance
    chartRef.current = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: heavyHitters.map(element => element.category),
        datasets: [
          {
            data: heavyHitters.map(element => element.amount),
            backgroundColor: colors,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });

    // Cleanup function to destroy the chart when component unmounts or data changes
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy(); // Properly destroy chart
        chartRef.current = null; // Set to null to avoid lingering references
      }
    };
  }, [heavyHitters]); // Effect depends on heavyHitters data

  return (
    <div>
      <canvas className="min-h-30rem" ref={canvasRef}></canvas> {/* Canvas is rendered */}
    </div>
  );
};

export default HeavyHitterPieChart;
