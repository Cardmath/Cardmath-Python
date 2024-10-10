import React from "react";
import { Chart, registerables } from "chart.js";
import "chartjs-adapter-moment";
import SliderComponent from "../SliderComponent";
import moment from "moment";
Chart.register(...registerables);

const LineChartComponent = (props) => {
  const { chartId, chartData, config } = props;
  const chartRef = React.useRef(null);
  const [data, setData] = React.useState(chartData);

  React.useEffect(() => {
    setData(chartData);
    chartRef.current && chartRef.current.destroy();
    chartRef.current = new Chart(document.getElementById(chartId), config);
    window[chartId] = chartRef.current;
  }, []);

  const handleChart = (value) => {
    console.log(value);
    window[chartId].options.scales.x.min = moment(chartData[value[0]].x);
    window[chartId].options.scales.x.max = moment(chartData[value[1]].x);
    window[chartId] && window[chartId].update();
  };

  return (
    <div>
      <div style={{ height: "250px", width: "100%" }}>
        <canvas id={chartId}></canvas>
      </div>
      <SliderComponent data={data} handleChart={handleChart} />
    </div>
  );
};

export default LineChartComponent;
