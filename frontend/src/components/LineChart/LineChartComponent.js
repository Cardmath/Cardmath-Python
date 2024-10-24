import React, { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";
import "chartjs-adapter-moment";
import SliderComponent from "../SliderComponent";
import moment from "moment";
Chart.register(...registerables);

const LineChartComponent = (props) => {
  const { chartData, config } = props;
  const chartRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // Destroy previous chart if it exists
    if (chartRef.current) {
      chartRef.current.destroy();
      chartRef.current = null; // Ensure no lingering chart reference
    }

    // Create new chart instance
    chartRef.current = new Chart(ctx, config);

    // Cleanup on component unmount or dependency change
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
        chartRef.current = null; // Ensure chart is fully cleared
      }
    };
  }, [chartData, config]); // Re-create chart when data or config changes

  const handleChart = (value) => {
    const chartInstance = chartRef.current;
    if (chartInstance) {
      chartInstance.options.scales.x.min = moment(chartData[value[0]]);
      chartInstance.options.scales.x.max = moment(chartData[value[1]]);
      chartInstance.update();
    }
  };

  return (
    <div>
      <div class="chart-container" style={{position: "relative", height:"40vh", width:"53vw" }} >
        <canvas id="chart" ref={canvasRef}></canvas>
      </div>
      {chartData && chartData.length > 0 && (
        <SliderComponent data={chartData} handleChart={handleChart} />
      )}
      </div>
  );
};

export default LineChartComponent;
