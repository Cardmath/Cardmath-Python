import React from "react";
import LineChartComponent from "./LineChartComponent";
import moment from "moment";
import SliderComponent from "../SliderComponent";

const LineChartWrapper = (props) => {
  const [xmin, setXmin] = React.useState("2013-04-28");
  const [xmax, setXmax] = React.useState("2014-06-28");

  let res = [
    { x: "2013-04-28", y: 135.98 },
    { x: "2013-04-29", y: 147.49 },
    { x: "2013-04-30", y: 146.93 },
    { x: "2013-05-01", y: 139.89 },
    { x: "2013-05-02", y: 125.6 },
    { x: "2013-05-03", y: 108.13 },
    { x: "2013-05-04", y: 115 },
    { x: "2013-05-05", y: 118.8 },
    { x: "2013-05-06", y: 124.66 },
    { x: "2013-05-07", y: 113.44 },
    { x: "2013-05-08", y: 115.78 },
    { x: "2013-05-11", y: 118.68 },
    { x: "2013-05-12", y: 117.45 },
    { x: "2013-05-13", y: 118.7 },
    { x: "2013-05-14", y: 119.8 },
    { x: "2013-05-15", y: 115.81 },
    { x: "2013-05-16", y: 118.76 },
    { x: "2013-05-17", y: 125.3 },
    { x: "2013-05-18", y: 125.25 },
    { x: "2013-05-19", y: 124.5 },
    { x: "2014-05-09", y: 113.46 },
    { x: "2014-05-10", y: 122 },
    { x: "2014-05-11", y: 118.68 },
    { x: "2014-05-12", y: 117.45 },
    { x: "2014-05-13", y: 118.7 },
    { x: "2014-05-14", y: 119.8 },
    { x: "2014-05-15", y: 115.81 },
    { x: "2014-05-16", y: 118.76 },
    { x: "2014-05-17", y: 125.3 }
  ];
  const config = {
    type: "line",
    data: {
      labels: res.map((e) => e.x),
      datasets: [
        {
          label: "Utilisation",
          data: res.map((e) => e.y),
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: "index"
      },
      plugins: {
        legend: false,
        autocolors: false,
        tooltip: {
          backgroundColor: "#fff",
          titlFontColor: "#000",
          titleColor: "#000",
          titleMarginBottom: 8,
          titleSpacing: 3,
          bodyColor: "#475059",
          borderColor: "#E3E3E3",
          borderWidth: 1,
          padding: 10,
          bodySpacing: 8,
          usePointStyle: true,
          bodyFont: {
            font: {
              size: 14,
              lineHeight: "19px",
              family: "'Open Sans'",
              style: "normal"
            }
          },
          filter: function (tooltipItem, data) {
            if (tooltipItem.parsed.y !== 0) {
              return true;
            }
          },
          callbacks: {
            labelPointStyle: function (context) {
              return {
                pointStyle: "circle",
                rotation: 0
              };
            },
            label: function (context) {
              var label = "  ";
              if (context !== null && context !== undefined && context !== "") {
                label = label + context.dataset.label;
                if (
                  context.parsed.y !== null &&
                  context.parsed.y !== undefined
                ) {
                  label += ": " + context.parsed.y;
                }
              }
              return label;
            }
          }
        }
      },
      scales: {
        x: {
          min: moment(xmin),
          max: moment(xmax),
          parse: false,
          distribution: "linear",
          type: "time",
          time: {
            unit: "day",
            displayFormats: {
              millisecond: "mmm dd",
              second: "mmm dd",
              minute: "mmm dd",
              hour: "HH:mm",
              day: "MMM DD yyyy",
              week: "mmm dd",
              month: "mmm dd",
              quarter: "mmm dd",
              year: "mmm dd"
            }
          },
          grid: {
            drawOnChartArea: false,
            tickWidth: 1,
            tickLength: 10,
            offset: true
          },
          display: true,
          autoSkip: false,
          ticks: {
            align: "center"
          }
        },
        y: {
          grid: {
            tickWidth: 0,
            drawBorder: false
          }
        }
      }
    }
  };

  return (
    <div>
      <LineChartComponent
        chartData={res}
        chartId={"linechart"}
        config={config}
      />
    </div>
  );
};

export default LineChartWrapper;
