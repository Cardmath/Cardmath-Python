import React, { useEffect, useState } from "react";
import LineChartComponent from "./LineChartComponent";
import moment from "moment";

const LineChartWrapper = ({ x, y_list, ready }) => {
  const [config, setConfig] = useState(null);

  const colors = [
    "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#00FFFF", "#FFA500", "#800080"
  ];

  useEffect(() => {
    if (ready && x.length) {
      const xmin = x[0];
      const xmax = x[x.length - 1];

      setConfig({
        type: "line",
        data: {
          labels: x,
          datasets: y_list.map((e, index) => ({
            label: e.name,
            data: e.moving_average,
            fill: false,
            borderColor: colors[index % colors.length],
            tension: 0.5,
          })),
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            intersect: false,
            mode: "index",
          },
          plugins: {
            legend: {
              display: true,
            },
            tooltip: {
              backgroundColor: "#fff",
              titleColor: "#000",
              bodyColor: "#475059",
              borderColor: "#E3E3E3",
              borderWidth: 1,
              padding: 10,
              bodySpacing: 8,
              usePointStyle: true,
              callbacks: {
                label: (context) => {
                  return `${context.dataset.label}: ${context.parsed.y || 0}`;
                },
              },
            },
          },
          scales: {
            x: {
              type: "time",
              min: moment(xmin),
              max: moment(xmax),
              time: {
                unit: "day",
                displayFormats: {
                  day: "MMM DD yyyy",
                },
              },
              grid: {
                drawOnChartArea: false,
              },
              title: {
                display: true,
                text: 'Date',
              },
            },
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
              },
              title: {
                display: true,
                text: 'Spending Amount',
              },
            },
          },
          title: {
            display: true,
            text: 'Category Moving Averages Over Time',
          },
        },
      });
      
    }
  }, [ready, x, y_list]);

  return <div>{ready && config && <LineChartComponent chartData={x} chartId="linechart" config={config} />}</div>;
};

export default LineChartWrapper;
